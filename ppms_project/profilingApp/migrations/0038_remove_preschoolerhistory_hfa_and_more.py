# Generated by Django 4.1.2 on 2022-12-08 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0037_preschoolerhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preschoolerhistory',
            name='hfa',
        ),
        migrations.RemoveField(
            model_name='preschoolerhistory',
            name='wfa',
        ),
        migrations.RemoveField(
            model_name='preschoolerhistory',
            name='whfa',
        ),
    ]
