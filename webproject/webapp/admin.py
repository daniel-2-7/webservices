from django.contrib import admin
from .models import ModuleInstance, Professor, Rating, Course

admin.site.register(ModuleInstance)
admin.site.register(Professor)
admin.site.register(Rating)
admin.site.register(Course)