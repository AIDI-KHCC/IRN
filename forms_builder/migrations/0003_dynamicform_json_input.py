# Generated by Django 5.1.2 on 2024-10-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "forms_builder",
            "0002_alter_dynamicform_options_alter_formfield_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="dynamicform",
            name="json_input",
            field=models.TextField(blank=True, null=True),
        ),
    ]