# Generated by Django 2.2.5 on 2019-10-25 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20191025_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team_mail',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='total_mark',
            new_name='mark',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='team_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='team',
            name='member',
            field=models.IntegerField(default=0, verbose_name='how many people in this team'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Team'),
        ),
    ]
