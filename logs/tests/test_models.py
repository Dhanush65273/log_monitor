import pytest
from django.utils import timezone
from logs.models import LogEntry, Anomaly

@pytest.mark.django_db
def test_logentry_creation():
    log = LogEntry.objects.create(
        timestamp=timezone.now(),
        service="auth",
        log_level="ERROR",
        message="login failed"
    )

    assert log.service == "auth"
    assert log.log_level == "ERROR"
    assert log.message == "login failed"


@pytest.mark.django_db
def test_anomaly_creation():
    anomaly = Anomaly.objects.create(
        service="auth",
        anomaly_type="High Error Rate",
        description="Too many auth errors",
        severity="HIGH"
    )

    assert anomaly.service == "auth"
    assert anomaly.severity == "HIGH"
