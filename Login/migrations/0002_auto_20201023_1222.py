# Generated by Django 3.1.2 on 2020-10-23 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='work_expirience',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='year_of_grad',
            field=models.IntegerField(default=2018),
        ),
    ]
