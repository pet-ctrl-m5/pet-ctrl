# Generated by Django 4.0.6 on 2022-07-18 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
