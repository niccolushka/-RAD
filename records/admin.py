"""Настройки административной панели."""
from django.contrib import admin

from .models import EEGAnalysisResult, EEGFile, EEGSession, Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Список пациентов с быстрым доступом к сеансам."""

    list_display = ("full_name", "birth_date")
    search_fields = ("full_name",)
    ordering = ("full_name",)


class EEGFileInline(admin.TabularInline):
    """Вложенная форма для файлов в сеансе ЭЭГ."""

    model = EEGFile
    extra = 1


class EEGAnalysisInline(admin.TabularInline):
    """Вложенная форма для результатов анализа."""

    model = EEGAnalysisResult
    extra = 0


@admin.register(EEGSession)
class EEGSessionAdmin(admin.ModelAdmin):
    """Управление сеансами обследований."""

    list_display = ("patient", "start_datetime", "technician", "duration_minutes")
    list_filter = ("technician", "start_datetime")
    search_fields = ("patient__full_name", "technician", "conclusion")
    inlines = [EEGFileInline, EEGAnalysisInline]


@admin.register(EEGFile)
class EEGFileAdmin(admin.ModelAdmin):
    """Управление загруженными файлами."""

    list_display = ("session", "uploaded_at", "description")
    search_fields = ("description", "file")


@admin.register(EEGAnalysisResult)
class EEGAnalysisResultAdmin(admin.ModelAdmin):
    """Управление результатами интеллектуального анализа."""

    list_display = ("session", "created_at", "emotion_label", "confidence", "model_name")
    list_filter = ("emotion_label", "created_at", "model_name")
    search_fields = ("session__patient__full_name", "model_name", "notes")
