"""Маршруты пользовательской части."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/", views.patients_list, name="patients_list"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("patients/new/", views.create_patient, name="create_patient"),
    path("sessions/new/", views.create_session, name="create_session"),
    path("files/upload/", views.upload_file, name="upload_file"),
    path("analysis/new/", views.create_analysis_result, name="create_analysis_result"),
]
