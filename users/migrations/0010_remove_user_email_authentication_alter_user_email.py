# Generated by Django 4.1.4 on 2023-02-27 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_blog_alter_user_github_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_authentication',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(editable=False, max_length=150),
        ),
    ]