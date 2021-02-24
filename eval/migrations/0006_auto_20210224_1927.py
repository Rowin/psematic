# Generated by Django 3.1.7 on 2021-02-24 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0005_auto_20210224_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='training_session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eval.trainingsession'),
        ),
        migrations.AddField(
            model_name='trainingsession',
            name='case_study_group_size',
            field=models.IntegerField(default=2, null=True),
        ),
    ]