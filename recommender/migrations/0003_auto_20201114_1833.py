# Generated by Django 3.1.3 on 2020-11-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20201114_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(),
        ),
    ]