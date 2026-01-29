from django.db import models


class LogEntry(models.Model):
    LOG_LEVEL_CHOICES = [
        ("INFO", "INFO"),
        ("WARN", "WARN"),
        ("ERROR", "ERROR"),
    ]

    timestamp = models.DateTimeField()
    service = models.CharField(max_length=50)
    log_level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
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

class Anomaly(models.Model):
    SEVERITY_CHOICES = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
    ]

    timestamp = models.DateTimeField(auto_now=True)
    service = models.CharField(max_length=50)
    anomaly_type = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["service", "anomaly_type"],
                name="unique_service_anomaly"
            )
        ]

    def __str__(self):
        return f"{self.service} | {self.anomaly_type} | {self.severity}"


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
    channel = models.CharField(max_length=20, choices=ALERT_CHANNELS)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="SENT")

    def __str__(self):
        return f"{self.channel} alert for {self.anomaly.anomaly_type}"
