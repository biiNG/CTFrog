from django.shortcuts import render

from challenge.models import Challenge,WhoFinishMe


def ChallengeHome(request):
    all_challenges = Challenge.objects.all()
    finished_challenges = Challenge.objects.filter(whofinishme__finished=True)
    return render(request,'challengehome.html',{
        'all' : all_challenges,
        'finished' : finished_challenges,
        },
    )

# def ChallengeDetail(request):
#
# def ChallengeResult(request):
