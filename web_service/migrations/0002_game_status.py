# Generated by Django 2.2.4 on 2019-08-08 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(default='NEW', max_length=50),
        ),
    ]