import json
from datetime import timedelta

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import LogEntry, Anomaly, Alert
from .alerts import send_email_alert
from .serializers import LogEntrySerializer

# Import detector
from .anomaly_engine import detect_anomalies


# =================================================
# Helper: Run detection + send mail
# =================================================
def trigger_anomaly_detection_and_alert():

    try:

        anomalies = detect_anomalies()   # LIST

        if anomalies:

            for anomaly in anomalies:
                send_email_alert(anomaly)
                print("📩 Mail sent:", anomaly.id, anomaly.anomaly_type)

        else:
            print("ℹ️ No new anomaly")


    except Exception as e:

        print("❌ Detection / Mail failed:", e)


# =================================================
# Home
# =================================================
def home(request):

    return render(request, "home.html")


# =================================================
# HTML – Send Log Page
# =================================================
def send_log_page(request):

    if request.method == "POST":

        service = request.POST.get("service") or request.POST.get("service_custom")

        message = request.POST.get("message") or request.POST.get("message_custom")

        LogEntry.objects.create(

            # 🔥 ALWAYS SERVER TIME
            timestamp=timezone.now(),

            service=service,

            log_level=request.POST.get("log_level"),

            message=message
        )


        # Run detector
        trigger_anomaly_detection_and_alert()


        return render(request, "send_log.html", {
            "success": True
        })


    return render(request, "send_log.html")


# =================================================
# POST API – JSON Ingest
# =================================================
@csrf_exempt
def ingest_log_api(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)


            LogEntry.objects.create(

                # 🔥 FORCE SERVER TIME
                timestamp=timezone.now(),

                service=data.get("service"),

                log_level=data.get("log_level"),

                message=data.get("message")
            )


            # Run detector
            trigger_anomaly_detection_and_alert()


            return JsonResponse(
                {"status": "log received"},
                status=201
            )


        except Exception as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )


    return JsonResponse(
        {"error": "Only POST allowed"},
        status=405
    )


# =================================================
# DRF API – Ingest
# =================================================
@api_view(["POST"])
def ingest_log(request):

    serializer = LogEntrySerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        # Run detector
        trigger_anomaly_detection_and_alert()


        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =================================================
# GET API – List Logs
# =================================================
def list_logs(request):

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


# =================================================
# HTML – Logs
# =================================================
def logs_page(request):

    logs = LogEntry.objects.all().order_by("-timestamp")

    return render(request, "logs_list.html", {
        "logs": logs
    })


# =================================================
# HTML – Filter Logs
# =================================================
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


    return render(request, "logs_filter.html", {
        "logs": logs
    })


# =================================================
# HTML – Anomalies
# =================================================
def anomalies_page(request):

    anomalies = Anomaly.objects.all().order_by("-timestamp")

    return render(request, "anomalies_list.html", {
        "anomalies": anomalies
    })


# =================================================
# Dashboard
# =================================================
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


# =================================================
# Alerts Page
# =================================================
def alerts_page(request):

    alerts = Alert.objects.select_related("anomaly").order_by("-sent_at")

    return render(request, "alerts_list.html", {
        "alerts": alerts
    })


# =================================================
# Test Email
# =================================================
def test_email_alert(request):

    anomaly = Anomaly.objects.last()

    if not anomaly:
        return HttpResponse("No anomaly found")


    try:

        send_email_alert(anomaly)

        return HttpResponse("✅ Email sent")


    except Exception as e:

        return HttpResponse(f"❌ Email failed: {e}")
