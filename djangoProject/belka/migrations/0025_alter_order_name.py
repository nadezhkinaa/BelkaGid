# Generated by Django 5.0.2 on 2024-06-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("belka", "0024_order_name_alter_userfavourites_favourite_places"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order", name="name", field=models.TextField(default="Заказ"),
        ),
    ]
