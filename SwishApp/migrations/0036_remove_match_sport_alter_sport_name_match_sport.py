# Generated by Django 5.0.6 on 2024-06-13 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0035_alter_sport_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='sport',
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Ping-pong', 'Ping-pong'), ('Football', 'Football'), ('Handball', 'Handball'), ('Tennis', 'Tennis'), ('Volleyball', 'Volleyball'), ('Basketball', 'Basketball')], max_length=20),
        ),
        migrations.AddField(
            model_name='match',
            name='sport',
            field=models.ManyToManyField(to='SwishApp.sport'),
        ),
    ]