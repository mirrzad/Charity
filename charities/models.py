from django.db import models
from django.conf import settings


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = [
        (0, 'elementary level'),
        (1, 'intermediate level'),
        (2, 'professional level'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)


class Charity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class Task(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    STATE_CHOICES = [
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done'),
    ]
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, models.CASCADE)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)
