from django.conf import settings
from django.core.mail import send_mail
from .models import Alert


def send_email_alert(anomaly):

    subject = f"[ALERT] {anomaly.anomaly_type}"

    message = f"""
⚠️ ANOMALY DETECTED ⚠️

Service   : {anomaly.service}
Type      : {anomaly.anomaly_type}
Severity  : {anomaly.severity}

Description:
{anomaly.description}

Time:
{anomaly.timestamp}

-- AI Log Monitoring System
"""

    try:

        # Send mail using Gmail SMTP
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.ALERT_RECEIVER_EMAIL],
            fail_silently=False,
        )

        # Save alert status
        Alert.objects.create(
            anomaly=anomaly,
            channel="EMAIL",
            status="SENT"
        )

        print("✅ Email sent via Gmail SMTP")

        return True


    except Exception as e:

        print("❌ Email error:", e)

        Alert.objects.create(
            anomaly=anomaly,
            channel="EMAIL",
            status="FAILED"
        )

        return False
