# Generated by Django 3.1.2 on 2020-11-27 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancies',
            name='link',
            field=models.URLField(default='www.jssstuniv.in', max_length=100),
        ),
    ]