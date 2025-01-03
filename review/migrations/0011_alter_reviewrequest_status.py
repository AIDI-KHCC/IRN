# Generated by Django 5.1.2 on 2024-11-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0010_alter_review_options_remove_review_is_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("submitted", "Submitted"),
                    ("under_review", "Under Review"),
                    ("revision_needed", "Unlocked for Revision"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                    ("suspended", "Suspended"),
                    ("withdrawn", "Withdrawn"),
                    ("expired", "Expired"),
                    ("archived", "Archived"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]
