# Generated by Django 5.0.2 on 2024-05-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0005_cafe_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="cafe", name="type", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="place", name="type", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="shop", name="type", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="cafe", name="address", field=models.TextField(),
        ),
    ]
