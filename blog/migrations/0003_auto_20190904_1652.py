# Generated by Django 2.2.2 on 2019-09-04 08:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190904_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticles',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='内容'),
        ),
    ]