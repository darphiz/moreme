# Generated by Django 3.0 on 2020-11-10 14:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0017_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
