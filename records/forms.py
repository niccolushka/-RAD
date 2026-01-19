"""Формы для пользовательских страниц."""
from django import forms

from .models import EEGAnalysisResult, EEGFile, EEGSession, Patient


class PatientForm(forms.ModelForm):
    """Форма создания/редактирования пациента."""

    class Meta:
        model = Patient
        fields = ["full_name", "birth_date", "contact_info"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "contact_info": forms.Textarea(attrs={"rows": 3}),
        }


class EEGSessionForm(forms.ModelForm):
    """Форма для регистрации сеанса ЭЭГ."""

    class Meta:
        model = EEGSession
        fields = ["patient", "start_datetime", "duration_minutes", "technician", "conclusion"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "conclusion": forms.Textarea(attrs={"rows": 3}),
        }


class EEGFileForm(forms.ModelForm):
    """Форма загрузки файлов обследования."""

    class Meta:
        model = EEGFile
        fields = ["session", "file", "description"]
        widgets = {"description": forms.TextInput(attrs={"placeholder": "Расшифровка, стимулы и т.п."})}


class EEGAnalysisResultForm(forms.ModelForm):
    """Форма добавления результатов интеллектуального анализа."""

    class Meta:
        model = EEGAnalysisResult
        fields = [
            "session",
            "model_name",
            "emotion_label",
            "confidence",
            "metrics",
            "visualization",
            "notes",
        ]
        widgets = {
            "metrics": forms.Textarea(attrs={"rows": 4, "placeholder": "JSON с признаками/метриками"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
