from django.contrib import admin

# Register your models here.

from .models import Composition, UserProfile

admin.site.register(Composition)
admin.site.register(UserProfile)


