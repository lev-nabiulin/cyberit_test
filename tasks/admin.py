from django.contrib import admin
from .models import CustomUser, Task, Work

admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Work)
