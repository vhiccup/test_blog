# Generated by Django 2.2.2 on 2019-09-05 08:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0008_auto_20190904_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='articles_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
