# Generated by Django 4.1.7 on 2023-03-10 10:36

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_salary_data_salary_month_salary_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='summ',
            field=models.IntegerField(default=django.contrib.auth.models.User),
        ),
        migrations.AlterField(
            model_name='salary',
            name='year',
            field=models.IntegerField(choices=[(2023, 2023)], default=None, null=True),
        ),
    ]
