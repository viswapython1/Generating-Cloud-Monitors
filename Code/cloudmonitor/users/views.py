from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from rest_framework import generics
import json
from .models import Account, Activity, ActivityStatus, Contact, ContactSource, ContactStatus
from .serializers import AccountSerializer, ActivitySerializer, ActivityStatusSerializer, ContactSerializer, ContactSourceSerializer, ContactStatusSerializer,UserFileModelSerializer
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework import generics
from django.http import JsonResponse
from .models import Account, Activity, ActivityStatus, Contact, ContactSource, ContactStatus
from .serializers import AccountSerializer, ActivitySerializer, ActivityStatusSerializer, ContactSerializer, ContactSourceSerializer, ContactStatusSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from .forms import CloudUserFrom,UserFileForm
from .models import CloudUsersModel
from django.contrib import messages
from rest_framework import status
from .models import CloudUsersModel,UserAppCreatModel,UserFileModel


#@api_view(['GET', 'POST'])
class AccountAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'

    def get(self, request):
        queryset = Account.objects.all()
        return Response({'profiles': queryset})

    def post(self, request, pk):
        print('AM going to Execute atleast once in my life')
        profile = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': Account})
        serializer.save()
        return redirect('account-list')

class ActivityAPIView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityStatusAPIView(generics.ListCreateAPIView):
    queryset = ActivityStatus.objects.all()
    serializer_class = ActivitySerializer

class ContactAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactStatusAPIView(generics.ListCreateAPIView):
    queryset = ContactStatus.objects.all()
    serializer_class = ContactSerializer

class ContactSourceAPIView(generics.ListCreateAPIView):
    queryset = ContactSource.objects.all()
    serializer_class = ContactSourceSerializer


def index(request):
    return render(request,'index.html',{})
def userlogin(request):
    return render(request,'userlogin.html',{})
def adminlogin(request):
    return render(request,'adminlogin.html',{})
def cloudlogin(request):
    return render(request,'cloudlogin.html',{})
def userregister(request):
    return render(request,'userregister.html',{})

@api_view(['GET', 'POST'])
def storeregistration(request):
    if request.method == 'POST':
        form = CloudUserFrom(request.POST)
        if form.is_valid():
            try:
                rslt = form.save()
                print("Form Result Status ", rslt)
                messages.success(request, 'You have been successfully registered')
            except:
                messages.success(request, 'Email Already Registerd')
            return  render(request, 'userregister.html',{})
        else:
            print("Invalid form")
    else:
        form = CloudUserFrom()
    return render(request, 'userregister.html', {'form': form})

def userlogincheck(request):
    if request.method == "POST":
        email = request.POST.get('cf-email')
        pswd = request.POST.get('cf-password')
        print("Email = ", email)
        try:
            check = CloudUsersModel.objects.get(email=email, password=pswd)
            request.session['id'] = check.id
            request.session['loggeduser'] = check.name
            request.session['email'] = check.email
            request.session['role']='user'
            status = check.status
            if status == "activated":
                print("User id At", check.id, status)
                return render(request, 'users/userpage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'userlogin.html')

            return render(request, 'userlogin.html', {})
        except:
            pass
    messages.success(request, 'Invalid Email id and password')
    return render(request, 'userlogin.html')



@api_view(['GET', 'PUT', 'DELETE','POST'])
def snippet_detail(request):
    role = request.session['role']

    usremail = request.session['email']
    try:
        snippet = UserFileModel.objects.filter(email=usremail)
        #print('Type is ',snippet.id)
    except CloudUsersModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        if role == 'user':
            print('Get Method Works Fine')
            usremail = request.session['email']
            queryset =  UserFileModel.objects.filter(email=usremail)
            serializer_class = UserFileModelSerializer
            print('Return Type is ',serializer_class)
            return render(request,'users/uploadedfiles.html',{'objects':queryset})
        elif role=='admin':
            queryset = UserFileModel.objects.all()
            serializer_class = UserFileModelSerializer
            return render(request, 'admin/adminuploadedfiles.html', {'objects': queryset})

        elif role =='cloud':
            queryset = UserFileModel.objects.all()
            serializer_class = UserFileModelSerializer
            return render(request, 'clouds/clouduploadedfiles.html', {'objects': queryset})

    elif request.method == 'PUT':
        print('PUT Method Works Fine')
        serializer = UserFileModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        print('DELETE Method Works Fine')
        #snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method=="POST":
        print('POST Method Works Fine')
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print('Invalid Form')
        return Response(status=status.HTTP_201_CREATED)

def logout(request):
    request.session.modified = True
    return render(request,'index.html',{})

def usercreateapp(request):
    usremail = request.session['email']
    dict = UserAppCreatModel.objects.filter(email=usremail)
    return render(request,'users/userappcreations.html',{'objects':dict})

def appcreaterequest(request):
    if request.method=='POST':
        usrname = request.POST.get('usrname')
        usremail = request.POST.get('usremail')
        appname = request.POST.get('appname')
        accesskey = request.POST.get('accesskey')
        secretkey = request.POST.get('secretkey')
        try:
            UserAppCreatModel.objects.create(name=usrname,email=usremail,appname=appname)
            messages.success(request, 'Your App creation Request is Under Process')
        except:
            messages.success(request, 'App Name Already exist')
            pass



        print(usrname,usremail,appname,accesskey,secretkey)
        dict = UserAppCreatModel.objects.filter(email=usremail)
    return render(request,'users/userappcreations.html',{'objects':dict})

def useruploadfile(request,appname):
    check = UserAppCreatModel.objects.get(appname=appname)
    acckey = check.accesskey
    secretkey = check.secretkey
    dict = {'appname':appname,'acckey':acckey,'secretkey':secretkey}
    return render(request,'users/uploaddatatocloud.html',dict)