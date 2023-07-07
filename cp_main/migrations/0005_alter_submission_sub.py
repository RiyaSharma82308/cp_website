# Generated by Django 4.2.2 on 2023-07-06 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cp_main", "0004_alter_submission_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="sub",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submission",
                to="cp_main.assignment",
            ),
        ),
    ]
