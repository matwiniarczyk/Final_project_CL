# Generated by Django 5.0.6 on 2024-06-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwishApp', '0005_rename_paid_parking_around_court_free_parking_around_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daysurvey',
            name='answer',
            field=models.IntegerField(choices=[(3, 'sunday'), (1, 'friday'), (2, 'saturday')]),
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(choices=[('Handball', 'Handball'), ('Volleyball', 'Volleyball'), ('Tennis', 'Tennis'), ('Ping-pong', 'Ping-pong'), ('Basketball', 'Basketball'), ('Football', 'Football')], max_length=20),
        ),
        migrations.AlterField(
            model_name='timesurvey',
            name='answer',
            field=models.IntegerField(choices=[(2, '16:00'), (1, '13:00'), (3, '19:00')]),
        ),
    ]
