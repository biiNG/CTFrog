# Generated by Django 2.2.5 on 2019-10-24 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191024_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=10, unique=True)),
                ('team_mail', models.EmailField(max_length=254, unique=True)),
                ('total_mark', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='ismanager',
            field=models.BooleanField(default=False, verbose_name='is team manager'),
        ),
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Team'),
        ),
    ]