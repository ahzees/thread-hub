# Generated by Django 5.0 on 2023-12-09 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0003_messages_content_messages_user_alter_messages_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_messages', to='thread.thread'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='messages',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thread', to='thread.messages'),
        ),
    ]
