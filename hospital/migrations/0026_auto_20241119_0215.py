# Generated by Django 3.0.5 on 2024-11-18 20:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0025_timeslot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='slot_time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 11, 19, 1, 57, 26, 749927)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeslot',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to=settings.AUTH_USER_MODEL),
        ),
    ]
