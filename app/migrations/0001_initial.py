# Generated by Django 3.0.8 on 2022-12-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoinData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinId', models.CharField(max_length=300, unique=True)),
                ('coin_name', models.CharField(max_length=300)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('last_updated', models.CharField(max_length=300)),
            ],
        ),
    ]