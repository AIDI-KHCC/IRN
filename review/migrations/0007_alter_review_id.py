# Generated by Django 5.1.2 on 2024-11-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0006_alter_reviewrequest_submission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
