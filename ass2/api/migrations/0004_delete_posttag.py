# Generated by Django 5.1 on 2024-10-09 16:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_posttag"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PostTag",
        ),
    ]
