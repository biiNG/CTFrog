# Generated by Django 2.2.6 on 2019-11-07 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0009_challenge_finishedtimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(blank=True, default='', max_length=200),
        ),
    ]