from django.shortcuts import render, redirect
from django.contrib import messages

from user import check_permission, models
from .forms import FlagForm
from challenge.models import Challenge, WhoFinishMe

import hashlib


def ChallengeHome(request):
    all_challenges = Challenge.objects.all()
    if request.session.get('is_login', None):
        username = request.session['username']
        finished_challenges = Challenge.objects.filter(whofinishme__user__name=username).filter(
            whofinishme__finished=True)
    else:
        finished_challenges = []
    pwn_challenges = []
    web_challenges = []
    re_challenges = []
    gen_challenges = []
    for c in all_challenges:
        if c.category == 'pwn':
            pwn_challenges.append(c)
        elif c.category == 'web':
            web_challenges.append(c)
        elif c.category == 're':
            re_challenges.append(c)
        elif c.category == 'gen':
            gen_challenges.append(c)

    return render(request, 'challengehome.html', {'pwn_challenges': pwn_challenges,
                                                  'web_challenges': web_challenges,
                                                  're_challenges': re_challenges,
                                                  'gen_challenges': gen_challenges,
                                                  'finished': finished_challenges,
                                                  },
                  )


def ChallengeDetail(request, primarykey):
    challenge = Challenge.objects.get(pk=primarykey)
    firstblood = WhoFinishMe.objects.filter(
        challenge=challenge).order_by('finishedTime').first()
    if request.session.get('is_login', False):
        username = request.session['username']
        user_existed = models.User.objects.get(name=username)
        finish = Challenge.objects.filter(whofinishme__challenge=challenge).filter(
            whofinishme__user=user_existed)
    else:
        finish = []
    form = FlagForm(request.POST)

    return render(request, 'challengedetail.html', {'title': challenge.title,
                                                    'category': challenge.category,
                                                    'description': challenge.description,
                                                    'bonus': challenge.bonus,
                                                    'flag': challenge.flag,
                                                    'file': challenge.file,
                                                    'finishtimes': challenge.finishedtimes,
                                                    'pk': primarykey,
                                                    'form': form,
                                                    'finish': finish,
                                                    'firstBlood': firstblood,
                                                    'URL': challenge.url,
                                                    },
                  )


# def ChallengeResult(request):

# def NoFlag(request):
#     messages.success(request, "你什么Flag也没有输入！")

@check_permission.check_login
def CheckFlag(request, primarykey):
    if request.method == "POST":
        form = FlagForm(request.POST)
        if form.is_bound:
            if form.is_valid():
                challenge = Challenge.objects.get(pk=primarykey)
                username = request.session['username']
                user_existed = models.User.objects.get(name=username)
                finish = WhoFinishMe.objects.filter(
                    challenge=challenge).filter(user=user_existed)

                hashFlag = hashlib.sha1(challenge.flag.encode("utf8"))
                hashFlagSubmit = hashlib.sha1(form.cleaned_data["Flag"].encode("utf8"))

                if (hashFlag.hexdigest() == hashFlagSubmit.hexdigest()) and (not finish):
                    F1 = WhoFinishMe(challenge=challenge,
                                     user=user_existed, finished=True)
                    F1.save()
                    challenge.finishedtimes += 1
                    challenge.save()
                    messages.add_message(
                        request, messages.SUCCESS, "Frog Caught！")
                    user_existed.mark += challenge.bonus
                    user_existed.submit_num += 1
                    user_existed.right_num += 1
                    user_existed.update_accuracy()
                    user_existed.save()
                    if request.session['is_in_team']:
                        teamname = request.session['teamname']
                        team = models.Team.objects.get(name=teamname)
                        team.score += challenge.bonus
                        team.save()
                else:
                    user_existed.submit_num += 1
                    user_existed.update_accuracy()
                    user_existed.save()
                    messages.add_message(request, messages.ERROR, "Frog is escaping......")

                return redirect('challenge-detail', primarykey=primarykey)
            else:
                messages.add_message(request, messages.WARNING, "你在乱输入些什么啊？")
    else:
        return redirect('challenge-detail', primarykey=primarykey)
