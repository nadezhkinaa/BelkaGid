# Generated by Django 5.0.2 on 2024-05-31 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0017_alter_event_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event", name="date", field=models.DateTimeField(),
        ),
    ]
