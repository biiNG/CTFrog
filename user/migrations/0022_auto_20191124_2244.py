# Generated by Django 2.2.6 on 2019-11-24 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student_id',
            field=models.IntegerField(verbose_name='The student id of the user'),
        ),
    ]
