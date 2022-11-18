# Generated by Django 4.1.2 on 2022-11-18 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0034_delete_barangayhealthworker'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarangayHealthWorker',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_validated', models.BooleanField(default=False)),
                ('bhw_barangay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilingApp.barangay')),
            ],
        ),
    ]