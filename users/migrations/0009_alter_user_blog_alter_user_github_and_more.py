# Generated by Django 4.1.4 on 2023-02-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_message_user_introduce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blog',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='introduce',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
    ]
