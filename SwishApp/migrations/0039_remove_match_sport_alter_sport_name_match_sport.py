# Generated by Django 5.0.6 on 2024-06-13 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0038_alter_sport_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='sport',
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Football', 'Football'), ('Volleyball', 'Volleyball'), ('Handball', 'Handball'), ('Ping-pong', 'Ping-pong'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis')], max_length=20),
        ),
        migrations.AddField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='SwishApp.sport'),
        ),
    ]