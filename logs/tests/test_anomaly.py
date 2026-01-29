import pytest
from logs.models import Anomaly

@pytest.mark.django_db
def test_anomaly_unique_constraint():
    Anomaly.objects.create(
        service="auth",
        anomaly_type="Spike",
        description="Spike detected",
        severity="LOW"
    )

    with pytest.raises(Exception):
        Anomaly.objects.create(
            service="auth",
            anomaly_type="Spike",
            description="Duplicate anomaly",
            severity="LOW"
        )
