# Generated by Django 5.0.2 on 2024-05-06 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0011_remove_cafe_address_remove_shop_short_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserFavourites",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("favourite_places", models.TextField()),
            ],
        ),
    ]
