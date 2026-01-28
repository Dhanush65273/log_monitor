from django.core.mail import send_mail
from django.conf import settings

from .models import Alert


def send_email_alert(anomaly):
    """
    Sends email ONLY ONCE per anomaly.
    If already sent, skip.
    """

    # 🔥 CHECK: email already sent?
    already_sent = Alert.objects.filter(
        anomaly=anomaly,
        channel="EMAIL"
    ).exists()

    if already_sent:
        # ❌ Don't spam
        print(f"Email already sent for anomaly {anomaly.id}")
        return

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
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ALERT_RECEIVER_EMAIL],
        fail_silently=False
    )

    # ✅ Save alert record (IMPORTANT)
    Alert.objects.create(
        anomaly=anomaly,
        channel="EMAIL",
        status="SENT"
    )
