# Generated by Django 3.1.4 on 2021-04-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0031_advertise_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.CharField(blank=True, choices=[(
                'ppa', 'PPA'), ('ppc', 'PPC')], default='ppa', max_length=10, null=True),
        ),
    ]
