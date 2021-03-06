# Generated by Django 2.1.7 on 2019-10-27 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20191027_1235'),
        ('challenge', '0006_auto_20191023_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='finishMe',
            field=models.ManyToManyField(through='challenge.WhoFinishMe', to='user.User'),
        ),
        migrations.AddField(
            model_name='whofinishme',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
