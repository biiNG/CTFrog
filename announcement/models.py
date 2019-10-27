from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class Announcement(models.Model):
    announcement_text = models.CharField(
        max_length=500, verbose_name='Announcement')
    pub_date = models.DateTimeField('date published')
    pub_user = models.CharField(
        max_length=100, verbose_name='user who publish')

    def __str__(self):
        return self.announcement_text+', published by '+self.pub_user

    def was_published_recently(self):
        '''
        if the announcement was published in the past 15 days, this will return true
        '''
        now = timezone.now()
        return now >= self.pub_date >= now-datetime.timedelta(days=15)

    # this will tell django sort by pub_date
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'
