# Generated by Django 2.0.7 on 2018-07-20 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180719_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='pw',
        ),
    ]
