from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.http import request, QueryDict
from bson import json_util, ObjectId
import json
import calendar
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from Teachers_Management.MongoCRUD import MongoTeachersManager

from Teachers_Management.serializers import NewTeacher

def addTeacher(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = NewTeacher(data=request.POST)
            if form.is_valid():
                data = dict(request.POST.dict())
                teachers_manager = MongoTeachersManager()
                print(data)
                if not teachers_manager.isTeacher(data, spec=True):
                    register = teachers_manager.addTeacher(data)
                    if register == True:
                        new_user = User()
                        new_user.set_password(data['lecturer_id'])
                        new_user.username = data['lecturer_id']
                        new_user.first_name, new_user.last_name = f"{data['first_name']} {data['last_name']}", '2'
                        new_user.email = data['email']
                        new_user.save()
                        
                        messages.info(request, "Teacher registered successfully")
                        return redirect('/teachers')

                    messages.info(request, "Something went wrong during registering")
                    return redirect('register-teacher')

                messages.info(request, "Already a Teacher, or redundant student's properties (eg. email)")
                return redirect('register-teacher')
        
            messages.error(request, form.errors)
            return redirect('register-teacher')
        
        if request.method == 'GET':
            return render(request, 'registerTeacher.html')