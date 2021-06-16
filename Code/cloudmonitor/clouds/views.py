from django.shortcuts import render,HttpResponse
from django.contrib import messages
from users.models import UserAppCreatModel
import string
import random

# Create your views here.

def cloudlogincheck(request):
    if request.method == "POST":
        usid = request.POST.get('name')
        pswd = request.POST.get('password')
        print("User ID is = ", usid)
        if usid == 'cloud' and pswd == 'cloud':
            request.session['role'] = 'cloud'
            return render(request, 'clouds/cloudhome.html')
        else:
            messages.success(request, 'Invalid Login Details')
    return render(request,'cloudlogin.html',{})

def activateuserapp(request):
    dict = UserAppCreatModel.objects.all()
    return render(request,'clouds/userappactivation.html',{'objects':dict})

def clouduserappactivations(request,appname):
    accessKey = genAccessToken(10)
    secretKey = genSecretKey(32)
    print('App Name = ', appname,' Access Key ',accessKey,' Secret Key ',secretKey)
    UserAppCreatModel.objects.filter(appname=appname).update(accesskey=accessKey,secretkey=secretKey)
    dict = UserAppCreatModel.objects.all()
    return render(request, 'clouds/userappactivation.html', {'objects': dict})

def genAccessToken(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def genSecretKey(stringLength=32):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

