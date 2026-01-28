from datetime import timedelta
from collections import Counter

from django.utils import timezone
from .models import LogEntry, Anomaly


ERROR_THRESHOLD = 5        # 5 errors
WINDOW_MINUTES = 5         # in last 5 minutes


def detect_anomalies():
    """
    Rule-based anomaly detection.
    - Updates existing anomaly
    - Never crashes due to duplicates
    """

    now = timezone.now()
    window_start = now - timedelta(minutes=WINDOW_MINUTES)

    recent_logs = LogEntry.objects.filter(
        timestamp__gte=window_start
    )

    error_logs = recent_logs.filter(log_level="ERROR")

    # --------------------------------------------------
    # RULE 1: High ERROR rate (global)
    # --------------------------------------------------
    error_count = error_logs.count()

    if error_count >= ERROR_THRESHOLD:
        Anomaly.objects.update_or_create(
            service="multiple",
            anomaly_type="High ERROR rate",
            defaults={
                "description": f"{error_count} ERROR logs in last 5 minutes",
                "severity": "HIGH",
                "timestamp": now,
            }
        )

    # --------------------------------------------------
    # RULE 2: Repeated service errors
    # --------------------------------------------------
    service_counter = Counter(
        error_logs.values_list("service", flat=True)
    )

    for service, count in service_counter.items():
        if count >= 3:
            Anomaly.objects.update_or_create(
                service=service,
                anomaly_type="Repeated service errors",
                defaults={
                    "description": f"{count} ERROR logs from service '{service}'",
                    "severity": "MEDIUM",
                    "timestamp": now,
                }
            )

    return True
