# Generated by Django 5.1.2 on 2024-11-05 20:45

from django.db import migrations, models

# Define the choices directly in the migration
SUBMISSION_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('under_review', 'Under Review'),
    ('rejected', 'Rejected'),
    ('accepted', 'Accepted'),
    ('revision_requested', 'Revision Requested'),
    ('closed', 'Closed'),
]

class Migration(migrations.Migration):

    dependencies = [
        ("submission", "0004_remove_coinvestigator_role_in_study_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusChoice",
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
                ("code", models.CharField(max_length=50, unique=True)),
                ("label", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Status Choice",
                "verbose_name_plural": "Status Choices",
                "ordering": ["order"],
            },
        ),
        migrations.AlterField(
            model_name="submission",
            name="status",
            field=models.CharField(
                choices=SUBMISSION_STATUS_CHOICES,
                max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="versionhistory",
            name="status",
            field=models.CharField(
                choices=SUBMISSION_STATUS_CHOICES,
                max_length=50
            ),
        ),
    ]
