from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
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
        srch = request.POST['srh']

        if srch:
            match= Prof.objects.filter(Q(name__icontains=srch)|Q(institute__icontains=srch)|Q(dept__icontains=srch)|Q(aor__icontains=srch))
            if match:
                return render(request, 'search.html', {'sr':match,'srch': request.POST['srh']})
            else:

                return render(request, 'search.html', {'sr': match, 'srch': request.POST['srh'],'messages':1})
        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'search.html')
