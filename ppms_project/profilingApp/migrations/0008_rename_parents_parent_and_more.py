# Generated by Django 4.1.2 on 2022-10-06 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0007_barangayhealthworker_bhw_barangay'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Parents',
            new_name='Parent',
        ),
        migrations.RenameModel(
            old_name='Preschoolers',
            new_name='Preschooler',
        ),
    ]
