# Generated manually для курсовой работы
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255, verbose_name="ФИО")),
                ("birth_date", models.DateField(verbose_name="Дата рождения")),
                ("contact_info", models.TextField(blank=True, verbose_name="Контакты/примечания")),
            ],
            options={
                "verbose_name": "Пациент",
                "verbose_name_plural": "Пациенты",
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="EEGSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_datetime", models.DateTimeField(verbose_name="Дата и время проведения")),
                ("duration_minutes", models.PositiveIntegerField(default=30, verbose_name="Длительность, мин")),
                ("technician", models.CharField(max_length=150, verbose_name="Оператор/врач")),
                ("conclusion", models.TextField(blank=True, verbose_name="Заключение")),
                (
                    "patient",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sessions", to="records.patient"),
                ),
            ],
            options={
                "verbose_name": "Сеанс ЭЭГ",
                "verbose_name_plural": "Сеансы ЭЭГ",
                "ordering": ["-start_datetime"],
            },
        ),
        migrations.CreateModel(
            name="EEGFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")),
                ("file", models.FileField(upload_to="eeg_files/", verbose_name="Файл")),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="Описание")),
                (
                    "session",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="files", to="records.eegsession"),
                ),
            ],
            options={
                "verbose_name": "Файл ЭЭГ",
                "verbose_name_plural": "Файлы ЭЭГ",
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
