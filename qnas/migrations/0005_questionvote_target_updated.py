# Generated by Django 4.1.4 on 2023-02-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnas', '0004_remove_answer_votes_remove_question_votes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionvote',
            name='target_updated',
            field=models.DateTimeField(null=True),
        ),
    ]