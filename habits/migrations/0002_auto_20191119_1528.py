# Generated by Django 2.2.7 on 2019-11-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='total_time',
            field=models.FloatField(default=0),
        ),
    ]
