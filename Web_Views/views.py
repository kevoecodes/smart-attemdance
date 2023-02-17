from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.http import request, QueryDict
from bson import json_util, ObjectId
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import calendar
from django.contrib import messages
from rest_framework.response import Response
from Attendance_Management.MongoCRUD import AttendanceManager
from Modules_Management.MongoCRUD import MongoModulesManager
from Staffs_Management.MongoCRUD import MongoStaffsManager

from Students_Management.MongoCRUD import MongoStudentsManager
from Teachers_Management.MongoCRUD import MongoTeachersManager
from Timetable_Management.MongoCRUD import MongoTImetableManager


def Dashboard_View(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.last_name == '3':
            att_data = AttendanceManager().getAttRange(None)
            avail = len(json.loads(json_util.dumps(AttendanceManager().getAttRange(None))))
            totalStudents = len(json.loads(json_util.dumps(MongoStudentsManager().getAllStudents())))
            currentClass = MongoTImetableManager().getCurrentClass()
            print(currentClass)

            return render(request, 'index.html', {
                "totalStudents": 0,
                "att_data": att_data,
                "avail": avail, "currentClass": currentClass, "totalStudents": totalStudents})

        elif request.user.is_authenticated and request.user.last_name == '2':
            print(request.user.username)
            teacher = MongoStaffsManager().getStaffData({"staff_id": request.user.username})
            print(teacher)
            modules = MongoModulesManager().getAllModules({"staff_id": teacher['staff_id']})
            print(modules)
            # att = AttendanceManager().getStudentAtt({"regNo": data['regNo']})
            # print(att)
            return render(request, 'teacher-profile.html', {"teacher": teacher, 'modules': modules})

    return redirect('login-page')


def Students_View(request):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "GET":
            students = MongoStudentsManager().getAllStudents()
            return render(request, 'students.html', {"students": students})

        if request.method == "POST":
            data = dict(request.POST.dict())
            students = MongoStudentsManager().getAllStudents(data)
            return render(request, 'students.html', {"students": students})

    return redirect('login-page')


def Teachers_View(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            teachers = MongoTeachersManager().getAllTeachers()
            print(teachers)
            return render(request, 'teachers.html', {"teachers": teachers})

        if request.method == "POST":
            data = dict(request.POST.dict())
            students = MongoStudentsManager().getAllStudents(data)
            return render(request, 'teaachers.html', {"teachers": students})

    return redirect('login-page')


def Teacher_Profile(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            data = dict(request.POST.dict())
            print(data)
            teacher = MongoTeachersManager().getTeacherData({"id": id})
            print(teacher)
            modules = MongoModulesManager().getAllModules({"lecturer_id": teacher['lecturer_id']})
            print(modules)
            # att = AttendanceManager().getStudentAtt({"regNo": data['regNo']})
            # print(att)
            return render(request, 'teacher-profile.html', {"teacher": teacher, 'id': id, 'modules': modules})

    return redirect('login-page')


def Student_Profile(request, id):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "GET":
            data = dict(request.POST.dict())
            print(data)
            student = MongoStudentsManager().getStudentData({"id": id})
            print(student)
            att = AttendanceManager().getStudentAtt({"regNo": student['regNo']})
            print(att)
            return render(request, 'profile.html', {"student": student, "id": id, "att": att})

    return redirect('login-page')


def updatePasswordTeacher(request, id=None):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'changePassword.html', {"id": id})

        if request.method == "POST":

            data = dict(request.POST.dict())
            del data['csrfmiddlewaretoken']
            teacher_manager = MongoTeachersManager()
            is_user = False
            if request.user.is_staff:
                is_user = teacher_manager.isTeacher({"id": id})
            else:
                is_user = teacher_manager.isTeacher({"lecturer_id": request.user.username})
            print(is_user)
            if is_user:
                user = User.objects.get(username=teacher_manager.teacher['lecturer_id'])
                if data['password1'] == data['password2']:
                    user.set_password(data['password1'])
                    user.save()
                    if id == None:
                        return redirect('/')
                    return redirect('/teacher/' + id)
                messages.info(request, "Posswords doesn't match")
                if id == None:
                    return redirect('/lecturer-change-password')
                return redirect('/lecturer-change-password/' + id)

    return redirect('login-pages')


def Class_Attendance(request, id=None):
    if request.user.is_authenticated:
        if request.method == "GET":
            if id == None:
                modules = json.loads(json_util.dumps(MongoModulesManager().getAllModules()))

                return render(request, 'class-attendance.html', {"att_avail": False, "modules": modules})
            else:
                module = MongoModulesManager().getModule({"id": id})
                att_data = AttendanceManager().getAtt(module['module_code'])

                timetable = MongoModulesManager().editModuleView({"module_code": module['module_code']})
                print(timetable['timetable'])
                # print(att_data)
                today = datetime.now(timezone(timedelta(hours=3))).day

                the_month = calendar.monthcalendar(2023, 2)

                rang = calendar.monthrange(2023, 2)
                rang = []
                the_data = []
                days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                for v in the_month:
                    for x in range(0, 7):
                        c = {}
                        if v[x] != 0:
                            rang.append(v[x])
                            c['day'] = v[x]
                            c['day_name'] = days[x]
                            if x == 6 or x == 5:
                                c['weekend'] = True

                            else:
                                c['weekend'] = False
                                print(c['day_name'])
                                if c['day_name'] in timetable['timetable']:
                                    c['is_class'] = True
                            the_data.append(c)

                print(the_data)
                return render(request, 'class-attendance.html',
                              {"the_data": the_data, "module": module, "att_data": att_data, "rang": rang,
                               "today": today, "att_avail": True})

        if request.method == "POST":
            data = dict(request.POST.dict())
            module = MongoModulesManager().getModule({"module_code": data['module_code']})

            return redirect(f'/class-attendance/{str(module["_id"])}')

    return redirect('login-page')


def Modules_View(request):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == 'GET':
            modules = MongoModulesManager().getAllModules()
            print(modules)

            return render(request, 'modules.html', {'modules': modules})

        if request.method == 'POST':
            pass

    return redirect('login-page')


def Create_Module(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'GET':
            return render(request, 'registerModule.html')

        if request.method == 'POST':
            print(request.POST)
            data = dict(request.POST.dict())
            print(data)
            module = MongoModulesManager()
            staff_manager = MongoStaffsManager()
            if not module.isModule(data):
                is_teacher = False
                print('Length', len(str(data['staff_id_2'])))
                if 'staff_id' in data and 'staff_id_2' in data and len(str(data['staff_id_2'])) > 0:
                    if staff_manager.isTeacher({'staff_id': data['staff_id_2']}) and staff_manager.isTeacher(
                            {'staff_id': data['staff_id']}):
                        is_teacher = True
                if 'staff_id' in data and 'staff_id_2' in data and len(str(data['staff_id_2'])) == 0:
                    if staff_manager.isTeacher({"staff_id": data['staff_id']}):
                        is_teacher = True

                if is_teacher:
                    if staff_manager.teacher['staff_type'] == 'Lecturer':
                        register = module.registerModule(data)
                        if register is True:
                            messages.info(request, 'Module registered successfully')
                            return redirect('/modules')
                        messages.info(request, 'Something went wrong')
                        return redirect('register-module')
                messages.info(request, 'Invalid Lecturer ID')
                return redirect('register-module')

            messages.info(request, 'Module already exists')
            return redirect('register-module')

    return redirect('login-page')


def editModule(request, id):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "GET":
            module_data = MongoModulesManager().editModuleView({"id": id})
            print(module_data)

            return render(request, 'registerModule.html', module_data)

        if request.method == "POST":
            data = dict(request.POST.dict())
            print(data)
            module = MongoModulesManager()
            lecturer_manager = MongoStaffsManager()
            if module.isModule(data):
                is_teacher = False
                print('Length', len(str(data['staff_id_2'])))
                if 'staff_id' in data and 'staff_id_2' in data and len(str(data['staff_id_2'])) > 0:
                    if lecturer_manager.isTeacher({'staff_id': data['staff_id_2']}) and lecturer_manager.isTeacher(
                            {'staff_id': data['staff_id']}):
                        is_teacher = True
                if 'staff_id' in data and 'staff_id_2' in data and len(str(data['staff_id_2'])) == 0:
                    if lecturer_manager.isTeacher({"staff_id": data['staff_id']}):
                        is_teacher = True

                if is_teacher:
                    register = module.editModule(data)
                    if register is True:
                        messages.info(request, 'Module Edited Successfully')
                        return redirect('/modules')

                messages.info(request, 'Invalid Lecturer ID')
                return redirect('/edit-module/' + id)
            messages.info(request, 'Something went wrong')

            return redirect('/edit-module/' + id)

    return redirect('login-page')


def editModuleView(request):
    if request.user.is_authenticated and request.user.is_staff or request.user.last_name == '3':
        if request.method == "POST":
            data = dict(request.POST.dict())
            module_data = MongoModulesManager().editModuleView(data)
            print(module_data)

            return render(request, 'registerModule.html', module_data)

    return redirect('login-page')


def deleteModule(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            data = dict(request.POST.dict())
            module = MongoModulesManager()
            if module.isModule(data):
                delete = module.deleteModule(data)
                return redirect('/modules')

    return redirect('login-page')

