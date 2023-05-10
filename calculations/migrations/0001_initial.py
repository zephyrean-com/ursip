# Generated by Django 4.2.1 on 2023-05-11 07:59

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Data2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('data_origin', models.CharField(choices=[('M', 'Fact'), ('P', 'Forecast')], max_length=1)),
                ('substance', models.CharField(choices=[('O', 'Oil'), ('L', 'Liq')], max_length=1)),
                ('value', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calculations.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Data1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('data_origin', models.CharField(choices=[('M', 'Fact'), ('P', 'Forecast')], max_length=1)),
                ('substance', models.CharField(choices=[('O', 'Oil'), ('L', 'Liq')], max_length=1)),
                ('value', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calculations.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]