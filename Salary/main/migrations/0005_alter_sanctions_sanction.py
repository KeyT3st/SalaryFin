# Generated by Django 4.1.7 on 2023-03-10 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_salary_summ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanctions',
            name='sanction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.sanction'),
        ),
    ]