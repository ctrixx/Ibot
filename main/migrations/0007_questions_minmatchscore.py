# Generated by Django 2.2.3 on 2019-08-20 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190819_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='MinMatchScore',
            field=models.IntegerField(default=0),
        ),
    ]