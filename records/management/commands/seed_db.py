from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.core.files.base import ContentFile

from records.models import Patient, EEGSession, EEGFile


SAMPLES = [
    {
        "full_name": "Иван Иванов",
        "birth_date": "1985-04-12",
        "contact_info": "тел: +7 900 111 22 33",
        "sessions": [
            {"days_ago": 10, "duration_minutes": 20, "technician": "Др. Смирнов", "conclusion": "Норма"},
            {"days_ago": 3, "duration_minutes": 30, "technician": "Др. Смирнов", "conclusion": "Снижение альфа"}
        ],
    },
    {
        "full_name": "Мария Петрова",
        "birth_date": "1992-09-01",
        "contact_info": "тел: +7 900 444 55 66",
        "sessions": [
            {"days_ago": 7, "duration_minutes": 25, "technician": "Др. Козлова", "conclusion": "Аномалия — бета"}
        ],
    },
    {
        "full_name": "Алексей Котов",
        "birth_date": "1978-12-20",
        "contact_info": "",
        "sessions": [
            {"days_ago": 1, "duration_minutes": 15, "technician": "Др. Иванов", "conclusion": "Шум/артефакты"}
        ],
    },
]


class Command(BaseCommand):
    help = "Seed DB: создать тестовых пациентов и сеансы ЭЭГ"

    @transaction.atomic
    def handle(self, *args, **options):
        created_patients = 0
        created_sessions = 0
        created_files = 0

        for s in SAMPLES:
            birth = date.fromisoformat(s["birth_date"])
            patient, p_created = Patient.objects.get_or_create(
                full_name=s["full_name"],
                defaults={"birth_date": birth, "contact_info": s["contact_info"]},
            )
            # обновляем поля, если уже был
            if not p_created:
                patient.birth_date = birth
                patient.contact_info = s["contact_info"]
                patient.save()

            if p_created:
                created_patients += 1

            for sess in s.get("sessions", []):
                start_dt = timezone.now() - timedelta(days=sess["days_ago"])
                session, sess_created = EEGSession.objects.get_or_create(
                    patient=patient,
                    start_datetime=start_dt,
                    defaults={
                        "duration_minutes": sess["duration_minutes"],
                        "technician": sess["technician"],
                        "conclusion": sess["conclusion"],
                    },
                )
                if not sess_created:
                    # обновить поля при необходимости
                    session.duration_minutes = sess["duration_minutes"]
                    session.technician = sess["technician"]
                    session.conclusion = sess["conclusion"]
                    session.save()

                if sess_created:
                    created_sessions += 1

                # создаём заглушечный EEGFile корректно, не обращаясь к динамическим related_name и id
                if not EEGFile.objects.filter(session=session).exists():
                    content = ContentFile(b"Placeholder EEG data\n", name=f"placeholder_session_{session.pk}.txt")
                    eeg_file = EEGFile(session=session, description="Тестовый файл (заглушка)")
                    eeg_file.file.save(content.name, content, save=True)
                    created_files += 1

        self.stdout.write(f"Пациентов создано/обновлено: {created_patients}")
        self.stdout.write(f"Сеансов создано/обновлено: {created_sessions}")
        self.stdout.write(f"Файлов создано: {created_files}")