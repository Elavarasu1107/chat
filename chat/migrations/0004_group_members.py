# Generated by Django 4.1.1 on 2022-11-05 03:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_user_options_alter_messages_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
