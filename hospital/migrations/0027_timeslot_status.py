# Generated by Django 3.0.5 on 2024-11-18 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0026_auto_20241119_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]