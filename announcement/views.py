from django.shortcuts import render
from django.views import generic
from .models import Announcement
from django.utils import timezone
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'announcement/index.html'
    context_object_name = 'announcement_list'

    def get_queryset(self):
        """return the last 5 posted questions"""
        return Announcement.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
