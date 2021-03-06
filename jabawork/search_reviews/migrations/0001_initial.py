# Generated by Django 3.1.3 on 2020-12-08 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Universities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviated', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=300)),
                ('link', models.CharField(max_length=300)),
                ('logo', models.CharField(max_length=50)),
                ('link_universitiy', models.CharField(max_length=46, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Opinions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200000)),
                ('date_opinion', models.CharField(max_length=40)),
                ('opinion', models.CharField(max_length=5)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_reviews.universities')),
            ],
        ),
    ]
