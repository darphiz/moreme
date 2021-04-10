# Generated by Django 3.0 on 2020-11-10 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20201110_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField(default=0)),
                ('ip_address', models.TextField(default='[]')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='articles.Article')),
            ],
        ),
    ]