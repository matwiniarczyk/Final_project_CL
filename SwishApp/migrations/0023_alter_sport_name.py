# Generated by Django 5.0.6 on 2024-06-13 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0022_alter_match_sport_alter_sport_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Football', 'Football'), ('Basketball', 'Basketball'), ('Ping-pong', 'Ping-pong'), ('Volleyball', 'Volleyball'), ('Tennis', 'Tennis'), ('Handball', 'Handball')], max_length=20),
        ),
    ]