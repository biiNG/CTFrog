from django.db import models


# Create your models here.
class Challenge(models.Model):
    title = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    bonus = models.IntegerField()
    href = models.URLField()

    #  finishMe = models.ManyToManyField(
    #      'account.User',  # TODO: choose the right models,need to import
    #      through='WhoFinishMe',
    #  )

    # class Meta:
    #     ordering = ['type']

    def __str__(self):
        return self.type + ' | ' + self.title


class WhoFinishMe(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    # user = models.ForeignKey(account.User, on_delete=models.CASCADE)  # TODO: choose the right models
    finished = models.BooleanField(default=False)
    finishedTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return
