from user.models import Team,User,ApplyMessage
u=User.objects.get(name='liu')
qs=[apply for apply in u.appliesreceived.all()]
print(qs)
first=qs[0]
first.delete()

a=ApplyMessage()
u1=User.objects.get(name='liu')
u2=User.objects.get(name='liu2')
u1.id
u2.id
a.sender=u1
a.receiver=u2
a.save()

