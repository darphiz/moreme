# Generated by Django 3.0 on 2020-11-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20201116_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='reject_reason',
            field=models.CharField(default='Your article violates the publishing guidlines', max_length=200),
        ),
    ]
