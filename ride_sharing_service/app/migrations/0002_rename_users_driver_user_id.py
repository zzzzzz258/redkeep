# Generated by Django 4.0.1 on 2022-01-23 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='users',
            new_name='user_id',
        ),
    ]
