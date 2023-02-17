# Generated by Django 2.2.26 on 2022-06-07 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default=None, max_length=256)),
                ('first_name', models.CharField(default=None, max_length=100)),
                ('mobileNo', models.CharField(default=None, max_length=100)),
                ('lecturer_id', models.CharField(default=None, max_length=100)),
                ('gender', models.CharField(default=None, max_length=100)),
                ('email', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]