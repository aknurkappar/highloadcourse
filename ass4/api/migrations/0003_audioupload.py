# Generated by Django 5.1 on 2024-11-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_customuser_secret_info"),
    ]

    operations = [
        migrations.CreateModel(
            name="AudioUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="audio_uploads/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="pending", max_length=15)),
                ("progress", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]