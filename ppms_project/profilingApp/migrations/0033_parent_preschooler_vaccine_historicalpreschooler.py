# Generated by Django 4.1.2 on 2022-11-18 12:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('profilingApp', '0032_remove_parent_user_remove_preschooler_parent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('barangay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilingApp.barangay')),
            ],
        ),
        migrations.CreateModel(
            name='Preschooler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('suffix_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('height', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(45.0), django.core.validators.MaxValueValidator(120.0)])),
                ('weight', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(28.0)])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('date_measured', models.DateField(blank=True, null=True)),
                ('health_problem', models.CharField(blank=True, max_length=500, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilingApp.parent')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_name', models.CharField(choices=[('BCG', 'BCG'), ('Hepatitis B', 'Hepatitis B'), ('Oral Poliovirus Vaccine', 'Oral Poliovirus Vaccine'), ('Pentavalent Vaccine', 'Pentavalent Vaccine'), ('Measles Containing Vaccines', 'Measles Containing Vaccines'), ('Tetanus Toxoid', 'Tetanus Toxoid'), ('Inactivated Polio Vaccine', 'Inactivated Polio Vaccine'), ('Measles Mumps - Rubella', 'Measles Mumps - Rubella')], max_length=500)),
                ('vax_dose', models.IntegerField()),
                ('vax_date', models.DateField(blank=True, null=True)),
                ('vax_remarks', models.DateField(blank=True, null=True)),
                ('vax_preschooler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilingApp.preschooler')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPreschooler',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('suffix_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('height', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(45.0), django.core.validators.MaxValueValidator(120.0)])),
                ('weight', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(28.0)])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('date_measured', models.DateField(blank=True, null=True)),
                ('health_problem', models.CharField(blank=True, max_length=500, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='profilingApp.parent')),
            ],
            options={
                'verbose_name': 'historical preschooler',
                'verbose_name_plural': 'historical preschoolers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
