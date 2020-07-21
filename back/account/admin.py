from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model

admin.site.register(models.Account)
admin.site.register(models.Transaction)
admin.site.register(models.Category)
admin.site.register(models.Tag)
