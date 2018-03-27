# Generated by Django 2.0.2 on 2018-03-21 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unevu', '0008_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='teacher',
            name='imageUrl',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='mobile',
            field=models.CharField(blank=True, max_length=14),
        ),
    ]