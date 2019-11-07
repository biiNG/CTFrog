from django.urls import path
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .import urls
from . import team_forms, models
from .check_permission import check_login, check_admin
from .models import Team, User, ApplyMessage, KickedMessage


def writetest(string):
    string = str(string)
    with open('1.txt', 'a') as f:
        f.write('\n'+string)


def clearteamsession(request):
    request.session.pop('is_in_team', None)
    request.session.pop('teamname', None)


@check_login
def register(request):
    username = request.session['username']
    if request.session['is_in_team']:
        return redirect('user:teamprofile')
    message = request.session.pop('message', None)
    if request.method == 'POST':
        register_form = team_forms.RegisterForm(request.POST)
        if register_form.is_valid():
            teamname = register_form.cleaned_data.get('team_name')
            teamemail = register_form.cleaned_data.get('team_mail')
            possible_same_name = models.Team.objects.filter(name='teamname')
            possible_same_email = models.Team.objects.filter(email='teamemail')
            if possible_same_name:
                request.session['message'] = '团队名已存在'
            elif possible_same_email:
                request.session['message'] = '邮箱已被注册'
            else:  # 邮箱和用户名均可用，则将注册成功
                newteam = models.Team()
                newteam.name = teamname
                newteam.email = teamemail
                newteam.admin = username
                newteam.save()
                # 该用户的相应权限也将变化，成为超级用户
                user = models.User.objects.get(name=username)
                user.issuperuser = True
                user.team = newteam
                user.save()
                request.session['teamname'] = newteam.name
                request.session['is_in_team'] = True
                return redirect('user:teamprofile')
    else:
        register_form = team_forms.RegisterForm()
    return render(request, 'team/register.html',
                  {'register_form': register_form})


@check_login
def profile(request):
    message = request.session.pop('message', None)
    templateurls = {'admin': 'team/profile/admin.html',
                    'member': 'team/profile/member.html',
                    'normal': 'team/profile/normal.html'}
    returntemplate = templateurls['normal']
    user = models.User.objects.get(name=request.session['username'])

    if request.session['is_in_team']:
        # 如果该用户有团队则进入该分支
        team = models.Team.objects.get(name=request.session['teamname'])
        teamscore = team.score
        allmembers = [u for u in team.user_set.all()]
        appliesreceived = [
            a for a in user.appliesreceived.all() if a.apply_state == 'unchecked']
        appliessent = [a for a in user.appliessent.all()]
        # writetest(str(team.user_set))
        variables = {'score': teamscore,
                     'members': allmembers,
                     'message': message,
                     'appliesreceived': appliesreceived,
                     'appliessent': appliessent,
                     'team_id': team.id}
        if user.issuperuser:
            return render(request, templateurls['admin'], variables)
        else:

            return render(request, templateurls['member'], variables)
    else:
        appliessent = [a for a in user.appliessent.all()]
        kickmessage = [k for k in user.kickedmessage.all()]
        return render(request, templateurls['normal'], {'appliessent': appliessent,'kickmessage':kickmessage})


@check_login
def join(request):
    '''
    获取团队列表后，择一申请加入
    '''
    username = request.session['username']
    teams = [models.Team.objects.get(name=t)
             for t in models.Team.objects.all()]
    try:
        user = models.User.objects.get(name=username)
    except:
        writetest('wrong')
    if request.method == 'POST':
        teamname = request.POST['team']
        team = models.Team.objects.get(name=teamname)
        admin = models.User.objects.get(name=team.admin)
        apply_admin_collected = [str(apply)
                                 for apply in admin.appliesreceived.all()]
        writetest(apply_admin_collected)
        if user.name in apply_admin_collected:
            request.session['message'] = '不能重复申请'
        else:
            apply = models.ApplyMessage()
            apply.receiver = admin
            apply.sender = user
            apply.team = teamname
            apply.save()
            request.session['message'] = '成功发送申请'
    message = request.session.pop('message', None)
    return render(request, 'team/join.html',
                  {'teams': teams, 'message': message})


@check_login
@check_admin
def applydenied(request, apply_id):
    try:
        apply = ApplyMessage.objects.get(pk=apply_id)
        apply.apply_state = 'denied'
        apply.save()

    except:
        session.request['message'] = 'no such apply'
    return redirect('user:teamprofile')


@check_login
@check_admin
def applyapproved(request, apply_id):
    cnt = 0
    try:
        apply = ApplyMessage.objects.get(pk=apply_id)
        sender = apply.sender
        team = Team.objects.get(name=request.session['teamname'])
        sender.team = team
        for a in sender.appliessent.all():#先将其他的申请置为不可用的状态
            a.apply_state='invalid'
            a.save()
        sender.save()
        apply.apply_state = 'approved'#将此申请置为可用的状态
        apply.save()
    except Exception as e:
        request.session['message'] = 'no such apply'
        writetest(e)
    finally:
        writetest(cnt)
    return redirect('user:teamprofile')


@check_login
@check_admin
def expel(request, user_id):
    if(request.method == "POST"):
        team = Team.objects.get(name=request.session['teamname'])
        user = User.objects.get(pk=user_id)
        user.team = None
        user.save()
        team.score -= user.score
        team.save()
        kickmessage = KickedMessage()#发送踢人的信息
        kickmessage.reason = request.POST['reason']
        kickmessage.team=request.session['teamname']
        kickmessage.kickeduser = user
        kickmessage.save()
        # 删掉此用户当时的申请
        admin=User.objects.get(name=request.session['username'])
        oldapply=admin.appliesreceived.get(sender=user)
        oldapply.delete()
        for otherapply in user.appliessent.filter(apply_state='invalid'):
            otherapply.apply_state='unchecked'
            otherapply.save()
        return redirect("user:teamprofile")

    return render(request, 'team/expel.html', {'id': user_id})


@check_login
@check_admin
def dismiss(request, team_id):
    team = Team.objects.get(pk=team_id)
    for u in team.user_set.all():
        if not u.issuperuser:
            u.team = None
            u.save()
            kickmessage = KickedMessage()
            kickmessage.reason = "team dismissed"
            kickmessage.save()
    superuser = User.objects.get(name=request.session['username'])
    superuser.issuperuser = False
    superuser.team = None
    for apply in superuser.appliesreceived.all():
        apply.delete()
    superuser.save()
    team.delete()
    request.session['message'] = "删除成功"
    clearteamsession(request)
    return redirect('user:profile')
