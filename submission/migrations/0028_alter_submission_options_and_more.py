# Generated by Django 5.1.3 on 2024-12-05 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submission", "0027_alter_submission_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="submission",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="submission",
            name="submission__status_832d62_idx",
        ),
        migrations.RemoveIndex(
            model_name="submission",
            name="submission__khcc_nu_653cf0_idx",
        ),
        migrations.RemoveIndex(
            model_name="submission",
            name="submission__primary_7bae28_idx",
        ),
        migrations.RemoveIndex(
            model_name="submission",
            name="submission__is_arch_0823ea_idx",
        ),
    ]
