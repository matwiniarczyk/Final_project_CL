from django.contrib.auth.models import User
from django.db import models


class Sport(models.Model):
    BB = 'BB'
    VB = 'VB'
    FB = 'FB'
    HB = 'HB'
    TN = 'TN'
    PP = 'PP'

    SPORT_CHOICES = {
        (BB, 'basketball'),
        (VB, 'volleyball'),
        (FB, 'football'),
        (HB, 'handball'),
        (TN, 'tennis'),
        (PP, 'ping-pong'),
    }
    name = models.CharField(max_length=2, choices=SPORT_CHOICES)


class Court(models.Model):
    name = models.CharField(max_length=50)
    localisation = models.CharField(max_length=50)
    paid_parking_around = models.BooleanField(default=False)
    intended_for = models.ManyToManyField(Sport)


class DaySurvey(models.Model):
    DAY_CHOICES = {
        (1, 'friday'),
        (2, 'saturday'),
        (3, 'sunday'),
    }
    answer = models.IntegerField(choices=DAY_CHOICES)


class TimeSurvey(models.Model):
    TIME_CHOICES = {
        (1, '13:00'),
        (2, '16:00'),
        (3, '19:00'),
    }
    answer = models.IntegerField(choices=TIME_CHOICES)


class Match(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    day = models.ForeignKey(DaySurvey, on_delete=models.CASCADE, default=None)
    time = models.ForeignKey(TimeSurvey, on_delete=models.CASCADE, default=None)


class Comment(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.court} {self.user} {self.date}"
