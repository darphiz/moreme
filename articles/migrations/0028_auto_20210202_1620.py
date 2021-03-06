# Generated by Django 2.2.10 on 2021-02-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0027_auto_20210118_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='updating_article',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='reject_reason',
            field=models.CharField(blank=True, default='Your article violates publishing guildlines', max_length=200, null=True),
        ),
    ]
