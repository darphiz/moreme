# Generated by Django 3.0 on 2020-10-08 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20201008_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
