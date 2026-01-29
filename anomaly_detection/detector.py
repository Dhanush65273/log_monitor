from datetime import timedelta
from django.utils import timezone
from logs.models import LogEntry, Anomaly
from .rules import DetectionRules


class AnomalyDetector:

    def __init__(self):
        self.rules = DetectionRules()
        self.time_window_minutes = DetectionRules.TIME_WINDOW

    def detect_all(self):
        now = timezone.now()
        last_n_minutes = now - timedelta(minutes=self.time_window_minutes)

        recent_logs = LogEntry.objects.filter(timestamp__gte=last_n_minutes)
        all_logs = LogEntry.objects.all()

        detected = []

        r1 = self.rules.check_high_error_rate(recent_logs)
        if r1.get("triggered"):
            detected.append(r1)

        detected += self.rules.check_repeated_service_errors(recent_logs)

        r3 = self.rules.check_high_warning_rate(recent_logs)
        if r3.get("triggered"):
            detected.append(r3)

        detected += self.rules.check_silent_service(all_logs, recent_logs)
        detected += self.rules.check_single_service_spam(recent_logs)

        for anomaly in detected:
            Anomaly.objects.create(
                service=anomaly["service"],
                anomaly_type=anomaly["anomaly_type"],
                description=anomaly["description"],
                severity=anomaly["severity"],
                timestamp=now,
            )

        return detected


def detect_anomalies():
    detector = AnomalyDetector()
    detector.detect_all()
    return True
