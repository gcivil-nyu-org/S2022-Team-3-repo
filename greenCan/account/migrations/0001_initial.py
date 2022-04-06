# Generated by Django 4.0.2 on 2022-03-20 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("recycle", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password"),),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("first_name", models.CharField(max_length=100, verbose_name="First name"),),
                ("last_name", models.CharField(max_length=100, verbose_name="Last name"),),
                (
                    "phone_number",
                    models.CharField(max_length=17, null=True, verbose_name="Phone number"),
                ),
                ("avatar", models.TextField(null=True, verbose_name="Avatar")),
                ("is_active", models.BooleanField(default=True)),
                ("staff", models.BooleanField(default=False)),
                ("admin", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "zipcode",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recycle.zipcode",
                        verbose_name="Zipcode",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="LoginAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID",
                    ),
                ),
                ("login_attempts", models.IntegerField(default=0)),
                ("timestamp", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
