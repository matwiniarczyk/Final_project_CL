# Generated by Django 5.0.6 on 2024-06-13 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0019_alter_sport_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SwishApp.sport'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Volleyball', 'Volleyball'), ('Basketball', 'Basketball'), ('Ping-pong', 'Ping-pong'), ('Handball', 'Handball'), ('Football', 'Football'), ('Tennis', 'Tennis')], max_length=20),
        ),
    ]
