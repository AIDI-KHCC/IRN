# Generated by Django 5.1.2 on 2024-10-28 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("forms_builder", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dynamicform",
            options={
                "verbose_name": "Dynamic Form",
                "verbose_name_plural": "Dynamic Forms",
            },
        ),
        migrations.AlterModelOptions(
            name="formfield",
            options={
                "verbose_name": "Form Field",
                "verbose_name_plural": "Form Fields",
            },
        ),
        migrations.AlterModelOptions(
            name="studytype",
            options={
                "verbose_name": "Study Type",
                "verbose_name_plural": "Study Types",
            },
        ),
    ]