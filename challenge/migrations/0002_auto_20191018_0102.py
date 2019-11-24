# Generated by Django 2.1.7 on 2019-10-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='challenge',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='challenge',
            name='file',
            field=models.FileField(max_length=200, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='challenge',
            name='flag',
            field=models.CharField(default='A_default_flag', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]