from django.shortcuts import render

from challenge.models import Challenge,WhoFinishMe


def ChallengeHome(request):
    all_challenges = Challenge.objects.all()
    finished_challenges = Challenge.objects.filter(whofinishme__finished=True)
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

    return render(request,'challengehome.html',{'pwn_challenge':pwn_challenges,
                                                'web_challenges':web_challenges,
                                                're_challenges':re_challenges,
                                                'gen_challenges':gen_challenges,
                                                'finished' : finished_challenges,
                                                },
    )

# def ChallengeDetail(request):
#
# def ChallengeResult(request):
