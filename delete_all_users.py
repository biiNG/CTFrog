from user.models import User, Team
for t in Team.objects.all():
    print(type(t))
    t.delete()
for u in User.objects.all():
    u.delete()
u=User.objects.get(pk=1)
