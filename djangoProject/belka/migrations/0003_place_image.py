# Generated by Django 5.0.2 on 2024-05-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0002_rename_cafes_cafe_rename_places_place"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="image",
            field=models.FilePathField(null=1, path="../static/img/"),
            preserve_default=1,
        ),
    ]
