from django.shortcuts import render
from kriti.forms import SignupForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.db.models import Q
from profs.models import Prof
import sqlite3
import os
module_dir = os.path.dirname(__file__)  # get current directory

def hello_world(request):
    if request.user.is_active:
        return render(request, 'home.html', {'user':request.user,})
    else:
        return render(request, 'home.html', {'user':[]})

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

def user_login(request):
    if request.user.is_active:
        return HttpResponseRedirect(reverse('hello_world'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('hello_world'))

                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return HttpResponse("Invalid login details given")
        else:
            return render(request, 'login.html', {})


def signup(request):
    if request.user.is_active:
        return HttpResponseRedirect(reverse('hello_world'))
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your Professearch account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('<h1>Please confirm your email address to complete the registration. <br>Check your mailbox</h1>')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('<h1>Thank you for your email confirmation. Now you can <a href="/login">login</a> your account.</h1>')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('hello_world'))
