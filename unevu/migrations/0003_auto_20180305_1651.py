# Generated by Django 2.0.2 on 2018-03-05 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unevu', '0002_auto_20180305_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='convener',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_convener', to='unevu.Teacher'),
        ),
        migrations.AlterField(
            model_name='course',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unevu.School'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='unevu.School'),
        ),
    ]