import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import LogEntry, Anomaly
from .anomaly_engine import detect_anomalies
from .alerts import send_email_alert


# -------------------------------------------------
# Helper: Auto anomaly detection + email alert
# -------------------------------------------------
def trigger_anomaly_detection_and_alert():
    """
    Runs anomaly detection and sends email
    ONLY for newly created anomalies.
    """

    # anomalies before detection
    before_ids = set(
        Anomaly.objects.values_list("id", flat=True)
    )

    # run detection
    detect_anomalies()

    # anomalies after detection
    after_ids = set(
        Anomaly.objects.values_list("id", flat=True)
    )

    # newly created anomalies
    new_ids = after_ids - before_ids

    for anomaly in Anomaly.objects.filter(id__in=new_ids):
        send_email_alert(anomaly)


# -------------------------------------------------
# Home page
# -------------------------------------------------
def home(request):
    return render(request, "home.html")


# -------------------------------------------------
# HTML – Send Log Page
# -------------------------------------------------
def send_log_page(request):
    if request.method == "POST":
        service = request.POST.get("service") or request.POST.get("service_custom")
        message = request.POST.get("message") or request.POST.get("message_custom")

        LogEntry.objects.create(
            timestamp=timezone.now(),   # always server time
            service=service,
            log_level=request.POST.get("log_level"),
            message=message
        )

        # 🔥 AUTO anomaly + AUTO email
        trigger_anomaly_detection_and_alert()

        return render(request, "send_log.html", {
            "success": True
        })

    return render(request, "send_log.html")


# -------------------------------------------------
# POST API – Log Ingestion
# -------------------------------------------------
@csrf_exempt
def ingest_log(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            timestamp = datetime.fromisoformat(data["timestamp"])
            if timezone.is_naive(timestamp):
                timestamp = timezone.make_aware(timestamp)

            LogEntry.objects.create(
                timestamp=timestamp,
                service=data["service"],
                log_level=data["log_level"],
                message=data["message"]
            )

            # 🔥 AUTO anomaly + AUTO email
            trigger_anomaly_detection_and_alert()

            return JsonResponse(
                {"status": "log received successfully"},
                status=201
            )

        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing field: {str(e)}"},
                status=400
            )

        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )

    return JsonResponse({"error": "Only POST allowed"}, status=405)


# -------------------------------------------------
# GET API – List Logs (JSON)
# -------------------------------------------------
def list_logs(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    logs = LogEntry.objects.all().order_by("-timestamp")

    service = request.GET.get("service")
    log_level = request.GET.get("log_level")
    date = request.GET.get("date")

    if service:
        logs = logs.filter(service=service)
    if log_level:
        logs = logs.filter(log_level=log_level)
    if date:
        logs = logs.filter(timestamp__date=date)

    data = []
    for log in logs:
        data.append({
            "timestamp": log.timestamp.isoformat(),
            "service": log.service,
            "log_level": log.log_level,
            "message": log.message,
        })

    return JsonResponse(data, safe=False)


# -------------------------------------------------
# HTML – View All Logs
# -------------------------------------------------
def logs_page(request):
    logs = LogEntry.objects.all().order_by("-timestamp")
    return render(request, "logs_list.html", {"logs": logs})


# -------------------------------------------------
# HTML – Filter Logs
# -------------------------------------------------
def logs_filter_page(request):
    logs = LogEntry.objects.all().order_by("-timestamp")

    service = request.GET.get("service")
    log_level = request.GET.get("log_level")
    date = request.GET.get("date")

    if service:
        logs = logs.filter(service=service)
    if log_level:
        logs = logs.filter(log_level=log_level)
    if date:
        logs = logs.filter(timestamp__date=date)

    return render(request, "logs_filter.html", {"logs": logs})


# -------------------------------------------------
# HTML – View Anomalies
# -------------------------------------------------
def anomalies_page(request):
    anomalies = Anomaly.objects.all().order_by("-timestamp")
    return render(request, "anomalies_list.html", {
        "anomalies": anomalies
    })


# -------------------------------------------------
# TEST – Email Alert
# -------------------------------------------------
def test_email_alert(request):
    anomaly = Anomaly.objects.last()
    if not anomaly:
        return HttpResponse("No anomaly found")

    send_email_alert(anomaly)
    return HttpResponse("Email alert sent")

from datetime import timedelta
from django.utils import timezone
from .models import LogEntry, Anomaly, Alert


def dashboard_page(request):
    now = timezone.now()
    last_5_min = now - timedelta(minutes=5)

    total_logs = LogEntry.objects.count()
    error_logs_5min = LogEntry.objects.filter(
        log_level="ERROR",
        timestamp__gte=last_5_min
    ).count()

    anomaly_count = Anomaly.objects.count()
    alert_count = Alert.objects.count()

    return render(request, "dashboard.html", {
        "total_logs": total_logs,
        "error_logs": error_logs_5min,
        "anomaly_count": anomaly_count,
        "alert_count": alert_count,
    })

def alerts_page(request):
    alerts = Alert.objects.select_related("anomaly").order_by("-sent_at")
    return render(request, "alerts_list.html", {
        "alerts": alerts
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogEntrySerializer

@api_view(["POST"])
def ingest_log(request):
    serializer = LogEntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
