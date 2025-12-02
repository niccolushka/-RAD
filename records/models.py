"""Модели домена ЭЭГ."""
from __future__ import annotations

from django.db import models
from django.core.validators import FileExtensionValidator


class Patient(models.Model):
    """Пациент, проходящий обследования."""

    full_name = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField("Дата рождения")
    contact_info = models.TextField("Контакты/примечания", blank=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self) -> str:  # pragma: no cover - удобный вывод в админке
        return self.full_name


class EEGSession(models.Model):
    """Сеанс ЭЭГ, привязанный к пациенту."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="sessions")
    start_datetime = models.DateTimeField("Дата и время проведения")
    duration_minutes = models.PositiveIntegerField("Длительность, мин", default=30)
    technician = models.CharField("Оператор/врач", max_length=150)
    conclusion = models.TextField("Заключение", blank=True)

    class Meta:
        ordering = ["-start_datetime"]
        verbose_name = "Сеанс ЭЭГ"
        verbose_name_plural = "Сеансы ЭЭГ"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.patient.full_name} — {self.start_datetime:%Y-%m-%d %H:%M}"


class EEGFile(models.Model):
    """Файл с результатами обследования."""

    session = models.ForeignKey(EEGSession, on_delete=models.CASCADE, related_name="files")
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)
    file = models.FileField("Файл", upload_to="eeg_files/", validators=[
        FileExtensionValidator(allowed_extensions=['edf', 'csv', 'txt'])
    ])
    description = models.CharField("Описание", max_length=255, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Файл ЭЭГ"
        verbose_name_plural = "Файлы ЭЭГ"

    def __str__(self) -> str:  # pragma: no cover
        return self.file.name
