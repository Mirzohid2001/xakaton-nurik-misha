# Generated by Django 5.0.7 on 2024-07-27 11:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_alter_review_unique_together_review_restaurant_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="district",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="district",
            name="name_uz",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="region",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="region",
            name="name_uz",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="description_uz",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="name_uz",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="description_uz",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="name_uz",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="worker",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="worker",
            name="name_uz",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.CreateModel(
            name="Location",
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
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
