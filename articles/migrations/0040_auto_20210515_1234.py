# Generated by Django 3.1.4 on 2021-05-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0039_auto_20210515_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(),
        ),
    ]
