from django.db import models


# Create your models here.
def challenge_file_path(instance):
    return 'ChallengeFiles/{}'.format(instance.category)


class Challenge(models.Model):
    title = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=10)
    description = models.CharField(max_length=200, blank=True, default="")
    bonus = models.IntegerField()
    flag = models.CharField(max_length=200)
    file = models.FileField(null=True, upload_to='ChallengeFiles/')

    #  finishMe = models.ManyToManyField(
    #      'account.User',  # TODO: choose the right models,need to import
    #      through='WhoFinishMe',
    #  )

    # class Meta:
    #     ordering = ['type']

    def __str__(self):
        return self.category + ' | ' + self.title


class WhoFinishMe(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    # user = models.ForeignKey(account.User, on_delete=models.CASCADE)  # TODO: choose the right models
    finished = models.BooleanField(default=False)
    finishedTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return
