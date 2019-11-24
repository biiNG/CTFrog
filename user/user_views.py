from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import user_forms, models
from .models import User, Team
import hashlib
from . import check_permission
from challenge.models import Challenge, WhoFinishMe
from .testing import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from CTFrog.settings import SECRET_KEY, EMAIL_FROM, EMAIL_HOST_USER
from django.core.mail import send_mail

'''
session中保存的变量：
username
user_id
is_login
'''


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    request.session.set_expiry(0)
    if request.session.get('is_login', False):
        return redirect('/home')

    message = request.session.pop('message', None)

    if request.method == 'POST':
        login_form = user_forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user_existed = models.User.objects.get(name=username)
            except:
                request.session['message'] = '无效的用户名'
                return redirect('user:login')
            if user_existed.password != hash_code(password):
                request.session['message'] = '密码错误'
                return redirect('user:login')
            elif user_existed.is_verified is False:
                request.session['message'] = "请先认证"
                return redirect("user:login")
            else:
                request.session['is_login'] = True
                # request.session['user_id']      = user_existed.id
                request.session['username'] = user_existed.name

                if user_existed.team:
                    request.session['teamname'] = user_existed.team.name
                    request.session['is_in_team'] = True
                else:
                    request.session['is_in_team'] = False
                # writetest(request.session['teamname'])

                return redirect('/home')
        else:
            request.session['message'] = '输入有误'
    else:
        login_form = user_forms.UserForm()
    return render(request, 'user/login.html', {'message': message, 'login_form': login_form})


def register(request):
    if request.session.get('is_login', None):
        return redirect('user:profile')
    message = request.session.pop('message', None)

    if request.method == 'POST':
        register_form = user_forms.RegisterForm(request.POST)
        if register_form.is_valid():
            all_data = register_form.cleaned_data
            username = all_data.get('username')
            password1 = all_data.get('password1')
            password2 = all_data.get('password2')
            email = all_data.get('email')
            sex = all_data.get('sex')
            student_id = all_data.get('studentid')
            real_name = all_data.get('realname')
            same_name_user = models.User.objects.filter(name=username)
            same_email_user = models.User.objects.filter(email=email)

            if password1 != password2:
                request.session['message'] = '两次密码不一致'
                return redirect('user:register')
            elif same_name_user:
                request.session['message'] = '用户名已经存在'
                return redirect('user:register')
            elif same_email_user:
                request.session['message'] = '该邮箱已经被注册了！'
                return redirect('user:register')
            else:
                # 用户名和邮件均可用的话进入该分支
                # 建立新用户
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.real_name = real_name
                new_user.student_id = student_id
                new_user.save()
                # 发送邮件
                s = Serializer(SECRET_KEY, 3600)
                token = s.dumps(new_user.pk)
                token = token.decode("utf-8")
                hostname = "localhost:8000/"
                protocal_used = r"http://"
                hypertext = '<a href="%s%suser/verify/%s" >%s%suser/verify/%s </a>' % (
                    protocal_used, hostname, token, protocal_used, hostname, token)
                send_message = 'please click this<br/>' + hypertext
                send_mail(subject="欢迎注册CTFrog", message="hallo", html_message=send_message, from_email=EMAIL_HOST_USER,
                          recipient_list=[email])

                request.session['message'] = '注册成功，一封确认邮件已发送至您的邮箱'
                return redirect('user:login')
        else:
            request.session['message'] = '输入有误'
            return redirect('user:register')
    else:
        register_form = user_forms.RegisterForm()
    return render(request, 'user/register.html', {'message': message, 'register_form': register_form})


def verify(request, token):
    s = Serializer(secret_key=SECRET_KEY, expires_in=3600)
    user_id = s.loads(token)
    try:
        user = User.objects.get(pk=user_id)
        writetest("i get user")
    except:
        return render(request, template_name='user/login.html')
    user.is_verified = True
    user.save()
    request.session['message'] = '验证成功'
    writetest("ok")
    return redirect('user:login')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('user:login')

    request.session.clear()
    # del request.session['is_login']
    return redirect("user:login")


@check_permission.check_login
def profile(request, username):
    '''将
    username、email、sex、form送入了表格中
    '''
    saved_user = models.User.objects.get(name=username)
    # with open('read.txt', 'w') as f:
    #     f.write(saved_user)
    finished_challenges = Challenge.objects.filter(whofinishme__user__name=username).filter(
        whofinishme__finished=True)
    pwn_challenges = []
    web_challenges = []
    re_challenges = []
    gen_challenges = []
    for c in finished_challenges:
        if c.category == 'pwn':
            pwn_challenges.append(c)
        elif c.category == 'web':
            web_challenges.append(c)
        elif c.category == 're':
            re_challenges.append(c)
        elif c.category == 'gen':
            gen_challenges.append(c)
    email = saved_user.email
    sex = saved_user.sex
    id = saved_user.student_id
    unchange = {'用户名': username, '邮箱': email, '性别': sex}
    if request.method == 'POST':
        form = user_forms.UpdateProfileForm(request.POST)
        if form.is_valid():
            student_id = int(form.cleaned_data.get('student_id'))
            saved_user.student_id = student_id
            saved_user.save()
            return render(request, 'user/profile.html', locals())

    form = user_forms.UpdateProfileForm(initial={'student_id': id})
    return render(request, 'user/profile.html', locals())


# def
@check_permission.check_login
def changepassword(request):
    username = request.session['username']
    saveduser = models.User.objects.get(name=username)
    message = request.session.pop('message', None)
    if request.method == 'POST':
        form = user_forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data.get('password1')
            pass2 = form.cleaned_data.get('password2')
            if pass1 != pass2:
                request.session['message'] = "两次输入不一致"
                return redirect("user:changepassword")
            else:
                saveduser.password = hash_code(pass1)
                saveduser.save()
                request.session['message'] = "修改成功"
                return redirect("user:changepassword")
        else:
            request.session['message'] = "输入有误"
            return redirect("user:changepassword")
    else:
        form = user_forms.ChangePasswordForm()
    return render(request, 'user/changepassword.html', {'form': form, 'message': message})
