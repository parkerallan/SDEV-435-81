# Generated by Django 4.2.16 on 2024-10-21 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]