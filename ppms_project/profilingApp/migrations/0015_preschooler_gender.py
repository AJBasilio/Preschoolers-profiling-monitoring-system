# Generated by Django 4.1.2 on 2022-10-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0014_customuser_phone_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='preschooler',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Gender: ', max_length=100),
        ),
    ]
