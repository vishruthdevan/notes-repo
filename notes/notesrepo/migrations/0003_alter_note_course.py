# Generated by Django 3.2.5 on 2021-08-01 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notesrepo', '0002_auto_20210731_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='notesrepo.course'),
        ),
    ]
