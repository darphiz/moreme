# Generated by Django 2.2.10 on 2021-04-27 15:43

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_bulkmail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkmail',
            name='message',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
