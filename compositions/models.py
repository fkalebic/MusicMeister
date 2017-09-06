from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    professor = models.BooleanField(default=False)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Composition(models.Model):
    graded = models.BooleanField(default=False)
    grade = models.PositiveSmallIntegerField(default=0)
    order = models.CharField(max_length=200)
    user = models.ForeignKey(User)