from datetime import timedelta
from collections import Counter
from django.utils import timezone


class DetectionRules:

    ERROR_THRESHOLD = 5
    SERVICE_ERROR_THRESHOLD = 3
    WARNING_THRESHOLD = 10
    TIME_WINDOW = 5

    MIN_TOTAL_LOGS_FOR_SPAM = 10
    MIN_SERVICE_LOGS_FOR_SPAM = 5
    SPAM_PERCENT_THRESHOLD = 0.7

    @staticmethod
    def check_high_error_rate(recent_logs):
        error_logs = recent_logs.filter(log_level="ERROR")

        if error_logs.count() >= DetectionRules.ERROR_THRESHOLD:
            return {
                "triggered": True,
                "service": "multiple",
                "anomaly_type": "High ERROR rate",
                "severity": "HIGH",
                "description": f"{error_logs.count()} ERROR logs in last {DetectionRules.TIME_WINDOW} minutes",
                "count": error_logs.count(),
            }

        return {"triggered": False}

    @staticmethod
    def check_repeated_service_errors(recent_logs):
        error_logs = recent_logs.filter(log_level="ERROR")
        service_counter = Counter(error_logs.values_list("service", flat=True))

        anomalies = []
        for service, count in service_counter.items():
            if count >= DetectionRules.SERVICE_ERROR_THRESHOLD:
                anomalies.append({
                    "triggered": True,
                    "service": service,
                    "anomaly_type": "Repeated service errors",
                    "severity": "MEDIUM",
                    "description": f'{count} ERROR logs from service "{service}"',
                    "count": count,
                })

        return anomalies

    @staticmethod
    def check_high_warning_rate(recent_logs):
        warning_logs = recent_logs.filter(log_level="WARN")

        if warning_logs.count() >= DetectionRules.WARNING_THRESHOLD:
            return {
                "triggered": True,
                "service": "multiple",
                "anomaly_type": "High WARNING rate",
                "severity": "MEDIUM",
                "description": f"{warning_logs.count()} WARNING logs in last {DetectionRules.TIME_WINDOW} minutes",
                "count": warning_logs.count(),
            }

        return {"triggered": False}

    @staticmethod
    def check_silent_service(all_logs, recent_logs):
        thirty_min_ago = timezone.now() - timedelta(minutes=30)

        active_before = set(
            all_logs.filter(
                timestamp__gte=thirty_min_ago,
                timestamp__lt=timezone.now() - timedelta(minutes=5),
            ).values_list("service", flat=True)
        )

        active_now = set(
            recent_logs.values_list("service", flat=True)
        )

        silent_services = active_before - active_now

        anomalies = []
        for service in silent_services:
            anomalies.append({
                "triggered": True,
                "service": service,
                "anomaly_type": "Service went silent",
                "severity": "MEDIUM",
                "description": f'Service "{service}" has not logged in last 5 minutes',
                "count": 0,
            })

        return anomalies

    @staticmethod
    def check_single_service_spam(recent_logs):
        service_counter = Counter(recent_logs.values_list("service", flat=True))
        total_logs = recent_logs.count()

        anomalies = []

        if total_logs < DetectionRules.MIN_TOTAL_LOGS_FOR_SPAM:
            return anomalies

        for service, count in service_counter.items():
            percentage = count / total_logs

            if (
                count >= DetectionRules.MIN_SERVICE_LOGS_FOR_SPAM
                and percentage >= DetectionRules.SPAM_PERCENT_THRESHOLD
            ):
                anomalies.append({
                    "triggered": True,
                    "service": service,
                    "anomaly_type": "Service log spam",
                    "severity": "LOW",
                    "description": (
                        f'Service "{service}" producing {count} logs '
                        f'({int(percentage * 100)}% of total)'
                    ),
                    "count": count,
                })

        return anomalies
