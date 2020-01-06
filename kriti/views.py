from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from profs.models import Prof
import sqlite3
import os
module_dir = os.path.dirname(__file__)  # get current directory

def hello_world(request):
    return render(request, 'home.html')
def pop(request):
    conn= sqlite3.connect(os.path.join(module_dir,"db.db"))
    c=conn.cursor()

    c.execute("SELECT * FROM Consolidated")
    Prof.objects.all().delete()
    for prof in c:
        p= Prof()
        if(prof[0]!=None and prof[1]!=None and prof[2]!=None):
            p.name,p.institute,p.dept,p.aor,p.phone,p.email,p.web=prof
            p.save()
    return HttpResponse('/')

def search(request):
    if request.method == 'POST':
        if (user["time"]-datetime.now()).total_seconds()<2 or user["verify"]==True:
            user["verify"]=True
            user["time"]=datetime.now()
            return HttpResponseRedirect('/verify_captcha')
        user["time"]=datetime.now()
        search = request.POST.get('search')
        page=1
    else:
        search=request.GET.get('search','')
        page = request.GET.get('page','1')
    matches= Prof.objects.filter(Q(name__icontains=search)|Q(institute__icontains=search)|Q(dept__icontains=search)|Q(aor__icontains=search))
    
    print("hello",page)
    paginator = Paginator(matches, 10)
    try:
        match = paginator.page(page)
    except PageNotAnInteger:
        match = paginator.page(1)
    except EmptyPage:
        match = paginator.page(paginator.num_pages)
    if match:
        return render(request, 'search.html', {'results':match,'search': search})
    else:

        return render(request, 'search.html', {'results': match, 'search': search,'fail':1})
    
    return render(request, 'search.html')
def verify_captcha(request):
