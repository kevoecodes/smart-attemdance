from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.http import request, QueryDict
from bson import json_util, ObjectId
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib import messages
from rest_framework.response import Response
from Attendance_Management.MongoCRUD import AttendanceManager
from Modules_Management.MongoCRUD import MongoModulesManager
from Staffs_Management.MongoCRUD import MongoStaffsManager
from .serializer import NewStaff
from Students_Management.MongoCRUD import MongoStudentsManager
from Teachers_Management.MongoCRUD import MongoTeachersManager
from Timetable_Management.MongoCRUD import MongoTImetableManager

def clear(request):
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass

def addLecturer(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = NewStaff(data=request.POST)
            if form.is_valid():
                data = dict(request.POST.dict())
                staff_manager = MongoStaffsManager()
                print(data)
                if not staff_manager.isTeacher(data, spec=True):
                    register = staff_manager.addTeacher(data)
                    if register == True:
                        new_user = User()
                        new_user.set_password(data['staff_id'])
                        new_user.username = data['staff_id']
                        new_user.first_name, new_user.last_name = f"{data['first_name']} {data['last_name']}", '2'
                        new_user.email = data['email']
                        new_user.save()
                        
                        #messages.info(request, "Lecturer registered successfully")
                        return redirect('/staffs')

                    messages.info(request, "Something went wrong during registering")
                    return redirect('register-teacher')

                messages.info(request, "Already a Lecturer, or redundant Lecturer's properties (eg. email)")
                return redirect('register-teacher')
        
            messages.error(request, form.errors)
            return redirect('/register-teacher')
        
        if request.method == 'GET':
            clear(request)
            return render(request, 'registerTeacher.html')

def addAssuarer(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = NewStaff(data=request.POST)
            if form.is_valid():
                data = dict(request.POST.dict())
                staff_manager = MongoStaffsManager()
                print(data)
                if not staff_manager.isAssuarer(data, spec=True):
                    register = staff_manager.addAssuarer(data)
                    if register == True:
                        new_user = User()
                        new_user.set_password(data['staff_id'])
                        new_user.username = data['staff_id']
                        new_user.first_name, new_user.last_name = f"{data['first_name']} {data['last_name']}", '3'
                        new_user.email = data['email']
                        new_user.save()
                        
                        #messages.info(request, "Assuarer registered successfully")
                        return redirect('/staffs')

                    messages.info(request, "Something went wrong during registering")
                    return redirect('register-assuarer')

                messages.info(request, "Already an Assuarer, or redundant Assuarer's properties (eg. email)")
                return redirect('/register-assuarer')
        
            messages.error(request, form.errors)
            return redirect('/register-assuarer')
        
        if request.method == 'GET':
            return render(request, 'registerAssuarer.html')


def Staffs_View(request):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "GET":
            
            if request.user.last_name == '3':
                staffs = MongoStaffsManager().getAllStaffs(staff={"staff_id": str(request.user.username)})
            else:
                staffs = MongoStaffsManager().getAllStaffs()
            print(staffs)
            return render(request, 'staffs.html', {"staffs": staffs})

        if request.method == "POST":
            data = dict(request.POST.dict())
            if request.user.last_name == '3':
                staffs = MongoStaffsManager().getAllStaffs(staff={"staff_id": str(request.user.username)})
            else:
                staffs = MongoStaffsManager().getAllStaffs()
            return render(request, 'staffs.html', {"staffs": staffs})


    return redirect('login-page')

def Staff_Profile(request, id):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "GET":
            staff_manager = MongoStaffsManager()
            data = dict(request.POST.dict())
            print(data)
            staff = staff_manager.getStaffData({"id": id})
            print(staff)
            if staff_manager.staff_type == 'Lecturer':
                modules = MongoModulesManager().getAllModules({"staff_id": staff['staff_id']})
                print(modules)
                return render(request, 'teacher-profile.html', {"teacher": staff, 'id':id, 'modules': modules})
            
            if staff_manager.staff_type == 'Assuarer':
                return render(request, 'assuarer-profile.html', {"assuarer": staff, 'id':id})


    return redirect('login-page')


def updatePasswordTeacher(request, id=None):
    if request.user.is_authenticated:
        if request.method == "GET":
            
            url = '/lecturer-change-password'   
            return render(request, 'changePassword.html', {"id": id, "url": url})

        if request.method == "POST":

            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            staff_manager = MongoStaffsManager()
            is_user = False
            if request.user.is_staff:
                is_user = staff_manager.isTeacher({"id": id})
            else:
                is_user = staff_manager.isTeacher({"staff_id": request.user.username})
            print(is_user)
            if is_user:
                user = User.objects.get(username=staff_manager.teacher['staff_id'])
                if data['password1'] == data['password2']:
                    user.set_password(data['password1'])
                    user.save()  
                    if id == None:
                        return redirect('/')
                    return redirect('/staff/'+id)
                messages.info(request, "Posswords doesn't match")
                if id == None:
                    return redirect('/lecturer-change-password')
                return redirect('/lecturer-change-password/'+id)
            
    return redirect('/login-page')

def updatePasswordAssuarer(request, id=None):
    if request.user.is_authenticated:
        if request.method == "GET":   
            url = '/assuarer-change-password'
            return render(request, 'changePassword.html', {"id": id, 'url': url})

        if request.method == "POST":

            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            staff_manager = MongoStaffsManager()
            is_user = False
            if request.user.is_staff:
                is_user = staff_manager.isAssuarer({"id": id})
            else:
                is_user = staff_manager.isAssuarer({"staff_id": request.user.username})
            print(is_user)
            if is_user:
                user = User.objects.get(username=staff_manager.assuarer['staff_id'])
                if data['password1'] == data['password2']:
                    user.set_password(data['password1'])
                    user.save()  
                    if id == None:
                        return redirect('/')
                    return redirect('/staff/'+id)
                messages.info(request, "Posswords doesn't match")
                if id == None:
                    return redirect('/assuarer-change-password')
                return redirect('/assuarer-change-password/'+id)
            
    return redirect('/login-page')

def editTeacher(request, id=None):
    if request.user.is_authenticated  and request.user.is_staff or request.user.last_name == '2':
        staff_manager = MongoStaffsManager()
        if request.method == "GET":
            staff = None
            if request.user.is_staff:
                staff = staff_manager.getStaffData({'id': id})
                url = '/lecturer-edit-credentials/'+id
            else:
                staff = staff_manager.getStaffData({"staff_id": request.user.username})
                url = '/lecturer-edit-credentials'
            if staff is not None:
               
               return render(request, 'registerTeacher.html', {"staff": staff, "url": url, "edit_mode": True})
            return redirect('/staffs')

        if request.method == "POST":
            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            staff_manager = MongoStaffsManager()
            print(data)
            is_user = False
            if request.user.is_staff:
                is_user = staff_manager.isTeacher({"id": id})
            else:
                is_user = staff_manager.isTeacher({"staff_id": request.user.username})
            print('Is Staff', is_user)
            if is_user:
                edit = staff_manager.editStaff(data)
                print('Edited', edit)
                if edit:
                    user = User.objects.get(username=staff_manager.teacher['staff_id'])
                    user.username = data['new_staff_id']
                    user.email =data['email']
                    user.first_name = f"{data['first_name']} {data['last_name']}"
                    user.save() 
                    if id == None:
                        return redirect('/')
                    return redirect('/staff/'+id)
            
            
    return redirect('/login-page')



def editAssuarer(request, id=None):
    if request.user.is_authenticated  and request.user.is_staff:
        staff_manager = MongoStaffsManager()
        if request.method == "GET":
            staff = None
            if request.user.is_staff:
                staff = staff_manager.getStaffData({'id': id})
                url = '/assuarer-edit-credentials/'+id
            else:
                staff = staff_manager.getStaffData({"staff_id": request.user.username})
                url = '/assuarer-edit-credentials'
            if staff is not None:
               
               return render(request, 'registerAssuarer.html', {"staff": staff, "url": url, "edit_mode": True})
            return redirect('/staffs')

        if request.method == "POST":
            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            staff_manager = MongoStaffsManager()
            is_user = False
            if request.user.is_staff:
                is_user = staff_manager.isAssuarer({"id": id})
            else:
                is_user = staff_manager.isAssuarer({"staff_id": request.user.username})
            print(is_user)
            if is_user:
                edit = staff_manager.editStaff(data)
                print('Edited', edit)
                if edit:
                    user = User.objects.get(username=staff_manager.assuarer['staff_id'])
                    user.username = data['new_staff_id']
                    user.email =data['email']
                    user.first_name = f"{data['first_name']} {data['last_name']}"
                    user.save() 
                    if id == None:
                        return redirect('/')
                    return redirect('/staff/'+id)
                  
            
    return redirect('/login-student')


def deleteStaff(request):
    if request.user.is_authenticated  and request.user.is_staff:
        if request.method == "POST":
            data = dict(request.POST.dict())
            if MongoStaffsManager().isStaff(data):
                delete = MongoStaffsManager().deleteStaff(data)
                user = User.objects.get(username=data['staff_id'])
                user.delete()

                return redirect('/staffs')
    return redirect('login-page')