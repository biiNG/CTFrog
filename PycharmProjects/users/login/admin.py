from django.contrib import admin

# Register your models here.

from . import models #'.': 从当前目录下导入models

admin.site.register(models.User)
