# Generated by Django 5.0.6 on 2024-06-13 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0032_alter_match_sport_alter_sport_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='SwishApp.sport'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Football', 'Football'), ('Volleyball', 'Volleyball'), ('Tennis', 'Tennis'), ('Ping-pong', 'Ping-pong'), ('Handball', 'Handball'), ('Basketball', 'Basketball')], max_length=20),
        ),
    ]
