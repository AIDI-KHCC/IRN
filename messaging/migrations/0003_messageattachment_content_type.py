# Generated by Django 5.1.2 on 2024-11-08 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0002_alter_message_thread_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="messageattachment",
            name="content_type",
            field=models.CharField(default="application/octet-stream", max_length=100),
        ),
    ]
