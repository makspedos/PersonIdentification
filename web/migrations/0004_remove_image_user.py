# Generated by Django 4.2.3 on 2023-10-10 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_image_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
    ]