# Generated by Django 5.0 on 2023-12-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='age',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
