# Generated by Django 4.1.3 on 2022-12-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='sold',
            field=models.BooleanField(null=True),
        ),
    ]