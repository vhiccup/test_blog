# Generated by Django 2.2.2 on 2019-07-27 02:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_articlepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 27, 2, 18, 48, 526931, tzinfo=utc)),
        ),
    ]
