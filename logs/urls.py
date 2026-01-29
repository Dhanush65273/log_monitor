from django.urls import path
from . import views

urlpatterns = [
    # ---------- API ----------
    path("logs/", views.ingest_log, name="ingest-log"),        # POST
    path("logs/list/", views.list_logs, name="list-logs"),     # GET JSON

    # ---------- HTML ----------
    path("", views.logs_page, name="logs-page"),               # /api/
    path("filter/", views.logs_filter_page, name="logs-filter"),
    path("send/", views.send_log_page, name="send-log"),
    path("anomalies/", views.anomalies_page, name="anomalies"),

    # ---------- TEST ----------
    path("test-email/", views.test_email_alert),
    path("dashboard/", views.dashboard_page, name="dashboard"),
    path("alerts/", views.alerts_page, name="alerts-page"),
]
