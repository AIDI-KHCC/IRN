# Generated by Django 5.1.2 on 2024-10-27 23:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0005_alter_message_respond_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="thread_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]