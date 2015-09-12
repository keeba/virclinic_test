from django.http import *
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import shutil

FILE_UPLOAD_DIR = 'media/'

@login_required
def root(request):
    return HttpResponseRedirect('/home')

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            error_dict={ 'login_error':1}
            return render_to_response('login.html',error_dict,context_instance=RequestContext(request))                   
    return render_to_response('login.html', context_instance=RequestContext(request))
    
def logout_user(request):
    logout(request) 
    return HttpResponseRedirect('/login')       
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_params = { "first_name":request.POST['first_name'],
                            "last_name":request.POST['last_name'],
                            "email":request.POST['email'], 
                          }
            User.objects.filter(pk=new_user.id).update(**user_params)
            username = request.POST['username']
            password = request.POST['password1']              
            user = authenticate(username=username,password=password)
            login(request, user)              
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })    

@login_required
def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))
    
def handle_uploaded_file(source,user_id):
    filepath = FILE_UPLOAD_DIR + 'user-'+str(user_id)+'.jpeg'
    print(filepath)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    return filepath  
def users(request,id):
    print(request.POST)
    if request.POST:
        print(request.FILES['myfile'])
        handle_uploaded_file(request.FILES['myfile'],request.user.id)
    return render_to_response('users.html', context_instance=RequestContext(request))          