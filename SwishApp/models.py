from django.contrib.auth.models import User
from django.db import models


class Sport(models.Model):
    BASKETBALL = 'Basketball'
    VOLLEYBALL = 'Volleyball'
    FOOTBALL = 'Football'
    HANDBALL = 'Handball'
    TENNIS = 'Tennis'
    PING_PONG = 'Ping-pong'

    SPORT_CHOICES = {
        (BASKETBALL, 'Basketball'),
        (VOLLEYBALL, 'Volleyball'),
        (FOOTBALL, 'Football'),
        (HANDBALL, 'Handball'),
        (TENNIS, 'Tennis'),
        (PING_PONG, 'Ping-pong'),
    }
    name = models.CharField(max_length=20, choices=SPORT_CHOICES)

    def __str__(self):
        return self.name


class Court(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    free_parking_around = models.BooleanField(default=False)
    intended_for = models.ManyToManyField(Sport)

    def __str__(self):
        return self.name


class Match(models.Model):
    TIME_CHOICES = (
        (1, '13:00'),
        (2, '16:00'),
        (3, '19:00'),
    )

    DAY_CHOICES = (
        (1, 'monday'),
        (2, 'tuesday'),
        (3, 'wednesday'),
        (4, 'thursday'),
        (5, 'friday'),
        (6, 'saturday'),
        (7, 'sunday'),
    )

    court = models.ManyToManyField(Court)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default=None)
    day = models.IntegerField(choices=DAY_CHOICES)
    time = models.IntegerField(choices=TIME_CHOICES)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_day_display()} {self.get_time_display()}"
    # get_FOO_display() - metoda dla pól które mają zdefiniowane choices


class Comment(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.court} {self.user} {self.date}"
