# Generated by Django 5.0.2 on 2024-05-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0014_rename_route_route_marshrut"),
    ]

    operations = [
        migrations.AddField(
            model_name="place", name="geo_x", field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="place", name="geo_y", field=models.FloatField(default=0),
        ),
    ]