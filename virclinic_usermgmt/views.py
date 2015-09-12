from django.http import *
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import shutil
from django.conf import settings

FILE_UPLOAD_DIR = 'static/'

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
    
def users(request,id):
    if request.POST and 'myfile' in request.FILES:
        push_picture_to_s3(request.FILES['myfile'],request.user.id)
    return render(request,'users.html',{})   
    
def push_picture_to_s3(source,id):
    try:
        import boto
        from boto.s3.key import Key
        # set boto lib debug to critical
        bucket_name = settings.BUCKET_NAME
        print(bucket_name+'worked')
        # connect to the bucket
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(bucket_name)
        print(conn)
        print(settings.AWS_ACCESS_KEY_ID)
        # go through each version of the file
        key = 'user-%s.png' % id
        print(key)
        #    fn = '/var/www/data/%s.png' % id
        # create a key to keep track of our file in the storage
        k = Key(bucket)
        k.key = key
        k.set_contents_from_file(source)
        # we need to make it public so it can be accessed publicly
        # using a URL like http://s3.amazonaws.com/bucket_name/key
        k.make_public()
        # remove the file from the web server
    except:
        print('error')
        pass
         