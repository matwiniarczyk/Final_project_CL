# Generated by Django 5.0.6 on 2024-06-13 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0030_alter_sport_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Basketball', 'Basketball'), ('Football', 'Football'), ('Handball', 'Handball'), ('Volleyball', 'Volleyball'), ('Tennis', 'Tennis'), ('Ping-pong', 'Ping-pong')], max_length=20),
        ),
    ]