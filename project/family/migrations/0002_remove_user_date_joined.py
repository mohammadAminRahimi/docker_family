# Generated by Django 3.2.5 on 2021-07-24 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
    ]
