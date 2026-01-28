from django.contrib import admin
from django.utils.html import format_html
from .models import LogEntry, Anomaly


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "service", "log_level_colored", "message_preview")
    list_filter = ("service", "log_level", "timestamp")
    search_fields = ("message", "service")
    readonly_fields = ("created_at", "timestamp")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    def log_level_colored(self, obj):
        """Display log level with color coding"""
        colors = {
            "INFO": "#3498db",     # Blue
            "WARN": "#f39c12",     # Orange
            "ERROR": "#e74c3c",    # Red
        }
        color = colors.get(obj.log_level, "#95a5a6")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.log_level
        )
    log_level_colored.short_description = "Log Level"

    def message_preview(self, obj):
        """Display truncated message"""
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
    message_preview.short_description = "Message"


@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "service", "anomaly_type", "severity_colored", "description_preview")
    list_filter = ("service", "severity", "timestamp")
    search_fields = ("service", "anomaly_type", "description")
    readonly_fields = ("timestamp",)
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    def severity_colored(self, obj):
        """Display severity with color coding"""
        colors = {
            "LOW": "#27ae60",      # Green
            "MEDIUM": "#f39c12",   # Orange
            "HIGH": "#e74c3c",     # Red
        }
        color = colors.get(obj.severity, "#95a5a6")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.severity
        )
    severity_colored.short_description = "Severity"

    def description_preview(self, obj):
        """Display truncated description"""
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
    description_preview.short_description = "Description"
