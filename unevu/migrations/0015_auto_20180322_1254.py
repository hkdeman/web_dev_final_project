# Generated by Django 2.0.2 on 2018-03-22 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unevu', '0014_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='username',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]