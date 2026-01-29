from rest_framework import serializers
from .models import LogEntry, Anomaly


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = [
            "timestamp",
            "service",
            "log_level",
            "message",
        ]


class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        fields = [
            "timestamp",
            "service",
            "anomaly_type",
            "description",
            "severity",
        ]
