# Generated by Django 4.2.3 on 2023-10-10 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='user',
            field=models.ForeignKey(db_column='user', default='', on_delete=django.db.models.deletion.DO_NOTHING, to='web.user'),
        ),
    ]