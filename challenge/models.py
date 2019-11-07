from django.db import models
from user.models import User

# Create your models here.
def challenge_file_path(instance):
    return 'ChallengeFiles/{}'.format(instance.category)


class Challenge(models.Model):
    title = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=10)
    description = models.TextField(max_length=200, blank=True, default="")
    bonus = models.IntegerField()
    flag = models.CharField(max_length=200)
    file = models.FileField(null=True, upload_to='ChallengeFiles/')

    finishMe = models.ManyToManyField(User,through='WhoFinishMe')
    finishedtimes = models.IntegerField(default=0)

    # class Meta:
    #     ordering = ['type']

    def __str__(self):
        return self.category + ' | ' + self.title


class WhoFinishMe(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    finished = models.BooleanField(default=False)
    finishedTime = models.DateTimeField(auto_now_add=True)
    #signature = models.CharField(default=user.name+' finish '+challenge.title,unique=True)

    def __str__(self):
        return self.user.name+' finish '+self.challenge.title
