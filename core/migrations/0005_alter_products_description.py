# Generated by Django 4.1.3 on 2022-11-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_products_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
