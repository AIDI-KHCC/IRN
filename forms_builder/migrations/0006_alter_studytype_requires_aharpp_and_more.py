# Generated by Django 5.1.2 on 2024-11-06 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms_builder", "0005_remove_studytype_requires_grant_management_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studytype",
            name="requires_aharpp",
            field=models.BooleanField(
                default=True,
                help_text="Requires AHRRP review",
                verbose_name="Requires AHRRP",
            ),
        ),
        migrations.AlterField(
            model_name="studytype",
            name="requires_irb",
            field=models.BooleanField(
                default=True,
                help_text="Requires IRB review",
                verbose_name="Requires IRB",
            ),
        ),
        migrations.AlterField(
            model_name="studytype",
            name="requires_research_council",
            field=models.BooleanField(
                default=True, help_text="Requires CR review", verbose_name="Requires CR"
            ),
        ),
    ]
