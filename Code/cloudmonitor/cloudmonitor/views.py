from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from users.models import UserFileModel
import os
from django.conf import settings
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
import os

from django.http import HttpResponse, Http404
from users.models import UserAppCreatModel

@api_view(['GET', 'PUT', 'DELETE','POST'])
def resturl(request,id):
    role = request.session['role']
    print('ROle is ',role)
    if request.method == 'GET':
        if role=='user':
            dict = {}
            data = UserFileModel.objects.get(id=id)
            filepath = data.userfile
            file = str(filepath).split("/")
            rd = open(os.path.join(settings.MEDIA_ROOT+'/media/', file[1]),'r',encoding='UTF-8',errors='ignore')
            filedata = rd.read()
            dict.update({'id':id,'filename':file[1],'seckey':data.secretkey,'fdata':filedata})
            return render(request,'users/editfilesdata.html',dict)
        elif role=='admin':
            print('Admin resturl works fine')
            dict = {}
            data = UserFileModel.objects.get(id=id)
            filepath = data.userfile
            file = str(filepath).split("/")
            rd = open(os.path.join(settings.MEDIA_ROOT + '/media/', file[1]), 'r', encoding='UTF-8', errors='ignore')
            filedata = rd.read()
            dict.update({'id': id, 'filename': file[1], 'seckey': data.secretkey, 'fdata': filedata})
            return render(request, 'admin/admineditfilesdata.html', dict)

        elif role=='cloud':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            print("Invalid URL")
    elif request.method =='POST':
        fileid = request.POST.get('fileid')
        filename = request.POST.get('filename')
        filedata = request.POST.get('filedata')
        with open(settings.MEDIA_ROOT+'/media' +'/'+filename, 'w+', encoding='UTF-8') as f:
            f.write(filedata)
        return Response(status=status.HTTP_200_OK)
        print('POST  Request Executed')
    print('User ID ',role,'File ID ',id)
    return HttpResponse('Am work fine')

def downloadfile(request,id):
    data = UserFileModel.objects.get(id=id)
    filepath = data.userfile
    # x1 = os.path.join(settings.MEDIA_ROOT+"//"+filepath)
    # print('X1 path = ',filepath)
    fppath = str(filepath).split("/")
    file_path = os.path.join(settings.MEDIA_ROOT+'/media/', fppath[1])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
@api_view(('GET',))
def deletefile(request,id):
    role = request.session['role']
    if role == 'user':
        data = UserFileModel.objects.get(id=id)
        data.delete()
        ##filepath = data.userfile
        #fpath = filepath #settings.MEDIA_ROOT+'/'+filepath
        #print('Removing FIle path is ',fpath)
        #os.remove(fpath)
        return Response(status=status.HTTP_200_OK)
    elif role =='admin':
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
    elif role =='cloud':
        data = UserFileModel.objects.get(id=id)
        data.delete()
        return Response(status = status.HTTP_200_OK)

@api_view(('GET',))
def uploadfile(request):
    role = request.session['role']
    if role =='user':
        usremail = request.session['email']
        dict = UserAppCreatModel.objects.filter(email=usremail)
        return  render(request,'users/uploadfile.html',{'objects':dict})
    elif role =='admin':
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

    elif role =='cloud':
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)