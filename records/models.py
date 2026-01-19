"""Модели домена ЭЭГ."""
from __future__ import annotations

from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


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


class EEGAnalysisResult(models.Model):
    """Результаты интеллектуального анализа ЭЭГ."""

    EMOTION_CHOICES = [
        ("neutral", "Нейтральное состояние"),
        ("calm", "Спокойствие"),
        ("joy", "Радость"),
        ("sadness", "Печаль"),
        ("stress", "Стресс"),
        ("fear", "Страх"),
        ("anger", "Гнев"),
        ("fatigue", "Утомление"),
    ]

    session = models.ForeignKey(
        EEGSession,
        on_delete=models.CASCADE,
        related_name="analysis_results",
        verbose_name="Сеанс ЭЭГ",
    )
    created_at = models.DateTimeField("Дата расчёта", auto_now_add=True)
    model_name = models.CharField("Модель/алгоритм", max_length=150)
    emotion_label = models.CharField("Класс эмоции", max_length=30, choices=EMOTION_CHOICES)
    confidence = models.FloatField(
        "Достоверность, 0-1",
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Оценка уверенности классификатора (0-1).",
    )
    metrics = models.JSONField("Метрики/признаки", blank=True, default=dict)
    visualization = models.FileField(
        "Визуализация",
        upload_to="eeg_visuals/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg", "svg", "pdf"]),
        ],
    )
    notes = models.TextField("Комментарий аналитика", blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Результат анализа"
        verbose_name_plural = "Результаты анализа"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.session} — {self.get_emotion_label_display()}"
