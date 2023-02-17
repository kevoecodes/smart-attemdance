from pickle import TRUE
from django.shortcuts import render, redirect
from django.http import request, QueryDict
from bson import json_util, ObjectId
from requests import delete
from rest_framework.views import APIView
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from Students_Management.MongoCRUD import MongoStudentsManager
from .serializaers import NewStudent
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response

def Register_Student(request):
    if request.user.is_authenticated  and request.user.is_staff:
        if request.method == 'GET':
            return render(request, 'registerStudent.html')
        if request.method == "POST":
            data = dict(request.POST.dict())
            student_manager = MongoStudentsManager()
            form = NewStudent(data=request.POST)
            if form.is_valid():
                if not MongoStudentsManager().isStudent(data):
                    register = student_manager.registerStudent(data)
                    if register == True:
                        new_user = User()
                        new_user.set_password(data['regNo'])
                        new_user.username = data['regNo']
                        new_user.first_name = f"{data['first_name']} {data['last_name']}"
                        new_user.last_name = '1'
                        new_user.email = data['email']
                        new_user.save()
                        
                        messages.info(request, "Student registered successfully")
                        return redirect('/fprint-register/'+str(student_manager.student_id))

                    messages.info(request, "Something went wrong during registering")
                    return redirect('register-student')

                messages.info(request, "Already a student, or redundant student's properties (eg. email)")
                return redirect('register-student')
        
            messages.error(request, form.errors)
            return redirect('register-student')
        
        if request.method == "GET":
            return render(request, 'registerStudent.html')

    return redirect('login-page')

def registerFingerPrint(request, id):
    if request.user.is_authenticated  and request.user.is_staff:
        student_manager = MongoStudentsManager()
        if request.method == 'GET':
            if student_manager.isStudent({"id": id}):
                data = {}
                data.update(student_manager.student)
                v = {}
                v['edit_mode'] = True
                data.update(v)
                print(data)
                return render(request, 'fingerprintRegister.html', {"student": data, "id": id})
        
        if request.method == "POST":
            data = dict(request.POST.dict())
            if MongoStudentsManager().isStudent(data):
                register = MongoStudentsManager().registerFingerprint(data)
                if register == True:
                    if 'edit_mode' in data:
                        
                        return redirect('/student-profile/'+ id)

                    messages.info(request, "Student's fingerprint registered successfully")
                    return redirect('/students')

                messages.info(request, "Something went wrong during registering")
                return redirect('/register-student')

            messages.info(request, "Student not found")
            return redirect('/register-student')


    return redirect('login-page')

def editStudent(request, id):
    if request.user.is_authenticated  and request.user.is_staff:
        student_manager = MongoStudentsManager()
        if request.method == "GET":
            if student_manager.isStudent({"id": id}):
                student = student_manager.student
                return render(request, 'registerStudent.html', {"student": student, "id": id, "edit_mode": True})

        if request.method == "POST":
            data = dict(request.POST.dict())
            print(data)
            edit = student_manager.editStudent(data)
            if edit == True:
                user = User.objects.get(username=data['regNo'])
                user.email = data['email']
                user.first_name = f"{data['first_name']} {data['last_name']}"
                user.username = data['new_regNo']
                user.save()

                return redirect('/student-profile/'+id)

    
    return redirect('login-page')

def deleteStudent(request):
    if request.user.is_authenticated  and request.user.is_staff:
        if request.method == "POST":
            data = dict(request.POST.dict())
            if MongoStudentsManager().isStudent(data):
                delete = MongoStudentsManager().deleteStudent(data)
                user = User.objects.get(username=data['regNo'])
                user.delete()

                return redirect('/view-students')
    return redirect('/login-page')


def updatePasswordStudent(request, id=None):
    if request.user.is_authenticated:
        if request.method == "GET":
            
            url = '/student-change-password'   
            return render(request, 'changePassword.html', {"id": id, "url": url})

        if request.method == "POST":

            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            student_manager = MongoStudentsManager()
            is_user = False
            if request.user.is_staff:
                is_user = student_manager.isStudent({"id": id})
            else:
                is_user = student_manager.isStudent({"regNo": request.user.username})
            print(is_user)
            if is_user:
                user = User.objects.get(username=student_manager.student['regNo'])
                if data['password1'] == data['password2']:
                    user.set_password(data['password1'])
                    user.save()  
                    if id == None:
                        return redirect('/')
                    return redirect('/student-profile/'+id)
                messages.info(request, "Posswords doesn't match")
                if id == None:
                    return redirect('/student-change-password')
                return redirect('/student-change-password/'+id)
            
    return redirect('login-page')


class AuthenticateStudent(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        user_dict = request.data
        user = QueryDict('', mutable=True)
        user.update(user_dict)

        the_user = authenticate(username=user['regNo'], password=user['regNo'])
        if the_user is not None:
            token = Token.objects.get_or_create(user=the_user)

            user_data = json.loads(json_util.dumps(MongoStudentsManager().getStudentData(user_dict)))
            feed = {
                "token": f'Token {str(token[0])}',
                "user": user_data
            }
            return Response(feed)
        else:
            return Response(None)  


