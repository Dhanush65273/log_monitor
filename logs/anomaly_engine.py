from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from logs.models import LogEntry, Anomaly


ERROR_THRESHOLD = 5
WINDOW_MINUTES = 5


class AnomalyDetector:

    def detect_all(self):

        now = timezone.now()
        window_start = now - timedelta(minutes=WINDOW_MINUTES)

        # ----------------------------
        # Errors in last 5 minutes
        # ----------------------------
        errors = LogEntry.objects.filter(
            log_level="ERROR",
            timestamp__gte=window_start
        )

        error_count = errors.count()

        print("⏱️ Window:", window_start, "→", now)
        print("❌ Errors:", error_count)


        # Not enough errors
        if error_count < ERROR_THRESHOLD:
            print("✅ Less than 5 errors")
            return False


        # ----------------------------
        # Active anomaly in this window?
        # ----------------------------
        active = Anomaly.objects.filter(
            anomaly_type="High ERROR rate",
            timestamp__gte=window_start
        ).first()


        # Update existing
        if active:

            active.description = f"{error_count} ERROR logs in last 5 minutes"
            active.timestamp = now
            active.save()

            print("🔁 Updated anomaly:", active.id)
            return active


        # ----------------------------
        # Create new anomaly
        # ----------------------------
        anomaly = Anomaly.objects.create(
            service="multiple",
            anomaly_type="High ERROR rate",
            description=f"{error_count} ERROR logs in last 5 minutes",
            severity="HIGH",
            timestamp=now,
        )

        print("🚨 New anomaly:", anomaly.id)

        # Send mail ONCE
        self.send_mail(anomaly)

        return anomaly


    def send_mail(self, anomaly):

        message = f"""
🚨 LOG MONITORING ALERT 🚨

Service  : {anomaly.service}
Type     : {anomaly.anomaly_type}
Severity : {anomaly.severity}
Time     : {anomaly.timestamp}

Description:
{anomaly.description}

-- AI Log Monitoring System
"""

        send_mail(
            subject="[ALERT] High Error Rate (Last 5 mins)",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ALERT_RECEIVER_EMAIL],
            fail_silently=False,
        )

        print("📩 Mail sent")


def detect_anomalies():

    detector = AnomalyDetector()
    return detector.detect_all()
