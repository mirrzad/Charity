from django.db import models
from django.conf import settings
from django.db.models import Q


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = [
        (0, 'elementary level'),
        (1, 'intermediate level'),
        (2, 'professional level'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Charity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Charities'

    def __str__(self):
        return self.user.username


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return Task.objects.filter(charity__user=user)

    def related_tasks_to_benefactor(self, user):
        return Task.objects.filter(assigned_benefactor__user=user)

    def all_related_tasks_to_user(self, user):
        return Task.objects.filter(
            Q(assigned_benefactor__user=user) |
            Q(charity__user=user) |
            Q(state__exact='P')
        )


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
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True, blank=True)
    charity = models.ForeignKey(Charity, models.SET_NULL, null=True, blank=True)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)

    objects = TaskManager()

    def __str__(self):
        return self.title
