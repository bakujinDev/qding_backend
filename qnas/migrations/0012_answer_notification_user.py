# Generated by Django 4.1.4 on 2023-02-25 23:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qnas', '0011_rename_votes_answervote_vote_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='notification_user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
