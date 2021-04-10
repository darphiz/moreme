# Generated by Django 3.0 on 2020-10-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20201008_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('published', 'Published'), ('rejected', 'Rejected')], default='pending', max_length=10, null=True),
        ),
    ]