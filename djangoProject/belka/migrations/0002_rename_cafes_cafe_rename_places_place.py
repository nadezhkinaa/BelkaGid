# Generated by Django 5.0.2 on 2024-05-02 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Cafes", new_name="Cafe",),
        migrations.RenameModel(old_name="Places", new_name="Place",),
    ]
