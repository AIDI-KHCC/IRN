# Generated by Django 5.1.3 on 2024-12-01 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submission", "0020_versionhistory_submitted_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="submitted_by",
        ),
        migrations.RemoveField(
            model_name="versionhistory",
            name="submitted_by",
        ),
    ]