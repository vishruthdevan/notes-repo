# Generated by Django 3.2.5 on 2021-07-29 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notesrepo', '0003_rename_code_course_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='slug',
            new_name='code',
        ),
    ]
