# Generated by Django 2.0.2 on 2018-03-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unevu', '0008_auto_20180320_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='avgRating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='noOfRatings',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='university',
            name='avgRating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='university',
            name='noOfRatings',
            field=models.FloatField(default=0),
        ),
    ]
