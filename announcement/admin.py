from django.contrib import admin
from .models import *
# Register your models here.


class AnnouncementAdmin(admin.ModelAdmin):
    exclude = ['pub_user', 'pub_date']
    ordering = ['-pub_date']
    list_display = ('announcement_text', 'pub_date',
                    'pub_user', 'was_published_recently')

    def save_model(self, request, obj, form, change):
        obj.pub_user = request.user.username
        obj.pub_date = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(Announcement, AnnouncementAdmin)
