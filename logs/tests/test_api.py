import pytest
from django.utils import timezone
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_log_ingestion_api():
    client = APIClient()

    payload = {
        "timestamp": timezone.now().isoformat(),
        "service": "auth",
        "log_level": "ERROR",
        "message": "invalid password"
    }

    response = client.post("/api/logs/", payload, format="json")

    assert response.status_code in [200, 201]
