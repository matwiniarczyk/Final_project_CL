# Generated by Django 5.0.6 on 2024-06-13 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0033_alter_match_sport_alter_sport_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='SwishApp.sport'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Handball', 'Handball'), ('Football', 'Football'), ('Tennis', 'Tennis'), ('Volleyball', 'Volleyball'), ('Basketball', 'Basketball'), ('Ping-pong', 'Ping-pong')], max_length=20),
        ),
    ]
