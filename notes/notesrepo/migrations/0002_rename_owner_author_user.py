# Generated by Django 3.2.5 on 2021-08-04 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notesrepo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='owner',
            new_name='user',
        ),
    ]
