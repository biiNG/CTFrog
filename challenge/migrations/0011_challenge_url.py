# Generated by Django 2.2.6 on 2019-11-19 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0010_auto_20191107_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
