# Generated by Django 3.2.5 on 2021-07-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesrepo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.SlugField(),
        ),
    ]
