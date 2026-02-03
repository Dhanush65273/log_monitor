from django.db import models
from django.utils import timezone


class LogEntry(models.Model):

    LOG_LEVEL_CHOICES = [
        ("INFO", "INFO"),
        ("WARN", "WARN"),
        ("ERROR", "ERROR"),
    ]

    # 🔥 Always server time
    timestamp = models.DateTimeField(default=timezone.now)

    service = models.CharField(max_length=50)

    log_level = models.CharField(
        max_length=10,
        choices=LOG_LEVEL_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["service"]),
            models.Index(fields=["log_level"]),
        ]

    def __str__(self):
        return f"{self.timestamp} | {self.service} | {self.log_level}"


# ==========================================
# ANOMALY
# ==========================================
class Anomaly(models.Model):

    SEVERITY_CHOICES = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
    ]

    # 🔥 FIXED (auto_now_add instead of auto_now)
    timestamp = models.DateTimeField(auto_now_add=True)

    service = models.CharField(max_length=50)

    anomaly_type = models.CharField(max_length=100)

    description = models.TextField()

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES
    )

    # ❌ NO UNIQUE CONSTRAINT (REMOVED)

    def __str__(self):
        return f"{self.service} | {self.anomaly_type} | {self.severity}"


# ==========================================
# ALERT
# ==========================================
class Alert(models.Model):

    ALERT_CHANNELS = [
        ("EMAIL", "Email"),
        ("TELEGRAM", "Telegram"),
    ]

    anomaly = models.ForeignKey(
        Anomaly,
        on_delete=models.CASCADE,
        related_name="alerts"
    )

    channel = models.CharField(
        max_length=20,
        choices=ALERT_CHANNELS
    )

    sent_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="SENT"
    )

    def __str__(self):
        return f"{self.channel} alert for {self.anomaly.anomaly_type}"
