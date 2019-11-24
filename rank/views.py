

from django.shortcuts import render

# Create your views here.
from user.models import User, Team
from django.core.paginator import Paginator
from django.views import View
class RankView(View):
    def get(self, request):
        ranktype = request.GET.get("type", None)
        keyword = request.GET.get("keyword", None)
        if ranktype == None:
            ranktype = "person"
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        if not page:
            page = 1
        if not page_size:
            page_size = 15
        page = int(page)
        ranktype = ranktype.strip()
        if ranktype == "team":
            all_data = Team.objects.all()
            all_data = all_data.order_by("-score")  # 查询所有的数据
        else:
            all_data = User.objects.all()
            all_data = all_data.order_by("-mark")  # 查询所有的数据
        rank = 1
        if keyword != None and keyword != "":
            keyword = keyword.strip()
            resultlist = []
            for i in all_data:
                i.id = rank
                rank += 1
                if keyword in i.name:
                    resultlist.append(i)
            all_page = Paginator(resultlist, int(page_size))  # 将数据和单页条数放到Paginator里面
            data = all_page.page(page)  # 获取具体页的
            return render(request, 'rank/rank.html', locals())
        else:
            for i in all_data:
                i.id = rank
                rank += 1
            all_page = Paginator(all_data, int(page_size))  # 将数据和单页条数放到Paginator里面
            data = all_page.page(page)  # 获取具体页的
            return render(request, 'rank/rank.html', locals())
