# Generated by Django 2.1.4 on 2019-10-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profs', '0002_auto_20191024_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prof',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='prof',
            name='web',
            field=models.CharField(max_length=512),
        ),
    ]
