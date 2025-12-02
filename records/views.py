"""Вспомогательные представления для пользовательского интерфейса."""
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from typing import TYPE_CHECKING, cast
from django.db.models.query import QuerySet

from .forms import EEGFileForm, EEGSessionForm, PatientForm
from .models import EEGFile, EEGSession, Patient

if TYPE_CHECKING:
    from .models import EEGSession


def dashboard(request):
    """Простая стартовая страница со сводкой."""
    context = {
        "patients_total": Patient.objects.count(),
        "sessions_total": EEGSession.objects.count(),
        "files_total": EEGFile.objects.count(),
        "latest_sessions": EEGSession.objects.select_related("patient")[:5],
    }
    return render(request, "records/dashboard.html", context)


def patients_list(request):
    """Список пациентов с количеством сеансов."""
    patients = Patient.objects.annotate(sessions_count=Count("sessions")).order_by("full_name")
    return render(request, "records/patients_list.html", {"patients": patients})


def patient_detail(request, pk: int):
    """Подробная карточка пациента."""
    patient = get_object_or_404(Patient, pk=pk)

    # безопасно получить queryset сеансов: сначала пытаемся взять related manager,
    # если его нет — делаем явный фильтр по модели (анализатор перестаёт жаловаться).
    related_mgr = getattr(patient, "sessions", None)
    if related_mgr is None:
        qs = EEGSession.objects.filter(patient=patient).prefetch_related("files")
    else:
        qs = related_mgr.prefetch_related("files").all()

    sessions = cast(QuerySet["EEGSession"], qs)
    return render(
        request,
        "records/patient_detail.html",
        {"patient": patient, "sessions": sessions},
    )


def create_patient(request):
    """Создание пациента через форму."""
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, "Пациент сохранён")
            return redirect(reverse("patient_detail", args=[patient.pk]))
    else:
        form = PatientForm()
    return render(request, "records/form_page.html", {"form": form, "title": "Новый пациент"})


def create_session(request):
    """Регистрация сеанса обследования."""
    if request.method == "POST":
        form = EEGSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            messages.success(request, "Сеанс добавлен")
            return redirect(reverse("patient_detail", args=[session.patient_id]))
    else:
        form = EEGSessionForm()
    return render(request, "records/form_page.html", {"form": form, "title": "Новый сеанс"})


def upload_file(request):
    """Загрузка файла к выбранному сеансу."""
    if request.method == "POST":
        form = EEGFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save()
            messages.success(request, "Файл загружен")
            return redirect(reverse("patient_detail", args=[file_obj.session.patient_id]))
    else:
        form = EEGFileForm()
    return render(request, "records/form_page.html", {"form": form, "title": "Загрузка файла"})
