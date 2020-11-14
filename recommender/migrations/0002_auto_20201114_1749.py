# Generated by Django 3.1.3 on 2020-11-14 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='MovieRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('num_votes', models.IntegerField()),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.movie')),
            ],
        ),
    ]
