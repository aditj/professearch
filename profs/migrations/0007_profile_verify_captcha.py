# Generated by Django 2.2.1 on 2020-01-07 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profs', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verify_captcha',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]