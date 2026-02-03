from django.db.models.signals import post_save
from django.dispatch import receiver

from logs.models import LogEntry
from anomaly_detection.detector import detect_anomalies


@receiver(post_save, sender=LogEntry)
def trigger_detection(sender, instance, created, **kwargs):

    if created and instance.log_level == "ERROR":
        print("🔥 ERROR saved → Running detector")
        detect_anomalies()
