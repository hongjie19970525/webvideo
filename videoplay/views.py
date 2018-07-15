from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader,Context
from django.shortcuts import render_to_response
import time
import random
import string
import hashlib
import requests
from django.core.cache import cache
from videoplay.models import Movie,User,UserComment,MoviePay
from videoplay.forms import UserForm,UserCommentForm,MoviePayForm


def checkhtml(request):
    check=loader.get_template("face_camera1.html")
    return HttpResponse(check.render())
    
def check(request):
    data=request.POST.get
    print(data)
    return HttpResponse("1")

def play(request,id):
    if request.method=='POST':
        print(request.POST)
    #url = 'http://' + request.get_host() + request.get_full_path()
    video_id = int(id)
    video_source = Movie.objects.get(id = video_id)
    t = loader.get_template("video.html")
    c = Context({"video_source": video_source, "video_id": video_id})
    return HttpResponse(t.render(c))

def regist(request):
    if request.method=='POST':
        uf_regist=UserForm(request.POST)
        if uf_regist.is_valid():
            username=uf_regist.cleaned_data.get('username')
            password=uf_regist.cleaned_data.get('password')
            User.objects.create(username=username,password=password)
            return HttpResponseRedirect('/')
        else:
            return render(request,'user_regist.html',{'danger':True})
    else:
        uf_regist=UserForm()
    user_regist=loader.get_template("user_regist.html")
    return HttpResponse(user_regist.render())
    
def login(request):
    if request.method=='POST':
        uf_login=UserForm(request.POST)
        if uf_login.is_valid():
            username=uf_login.cleaned_data['username']
            password=uf_login.cleaned_data['password']
            try:
                User.objects.get(username=username)
            except:
                return render_to_response('user_login.html',{'userName_error':True})
            user=User.objects.filter(username__exact=username,password__exact=password)
            if user:
                response=HttpResponseRedirect('/movie/')
                response.set_cookie('username',username)
                return response
            elif password!=User.objects.get(username=username).password:
                return render_to_response('user_login.html',{'userPassword_error':True})
        else:
            return render_to_response('user_login.html', {'userForm_error': True})
    else:
        uf_login = UserForm()
    user_login = loader.get_template("user_login.html")
    return HttpResponse(user_login.render())

def index(request):
    username=request.COOKIES.get('username',None)
    request.session['comment_username']=username
    if username!=None:
        return render_to_response('index.html',{'username':username})
    else:
        return render_to_response('index.html',{'error':True})

from rest_framework import viewsets
from videoplay.models import Movie
from videoplay.serializers import MovieSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer