from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Submission)