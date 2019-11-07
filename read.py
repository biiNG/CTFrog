from user.models import Team, User, ApplyMessage, KickedMessage
u=User()
u.save()
u
u.delete()
team=Team.objects.get(name='liu_team')
team.user_set.all()