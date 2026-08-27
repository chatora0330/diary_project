from datetime import datetime
from zoneinfo import ZoneInfo

from django.shortcuts import redirect, render
from django.views import View

from .forms import PageForm


class IndexView(View):
    def get(self, request):
        datetime_now = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d %H:%M:%S")
        
        return render(
            request, 
            "diary/index.html",
            {"datetime_now": datetime_now}
        )
    
class PageCreateView(View):
    def get(self, request):
        form = PageForm()
        return render(request, "diary/page_form.html", {"form": form})

    def post(self, request):
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("diary:index")
        return render(request, "diary/page_form.html", {"form": form})
    
    
index = IndexView.as_view()
page_create = PageCreateView.as_view()