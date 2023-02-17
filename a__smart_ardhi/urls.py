
from django.contrib import admin
from django.urls import path, include
from Attendance_Management.views import GetStudentAttendance
from Authentications.views import Login_View, Logout
from Device_Management.views import FPrintStudentReg, StudentAtt
from Modules_Management.views import GetStudentMondules
from Staffs_Management.views import Staff_Profile, Staffs_View, addAssuarer, addLecturer, deleteStaff, editAssuarer, editTeacher, updatePasswordAssuarer, updatePasswordTeacher
from Students_Management.views import AuthenticateStudent, Register_Student, deleteStudent, editStudent, registerFingerPrint, updatePasswordStudent
from Web_Views.views import Class_Attendance, Create_Module, Dashboard_View, Modules_View, Students_View, Student_Profile, Teacher_Profile, deleteModule, editModule


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("", Dashboard_View, name='Dashboard page'),
    path("login-page", Login_View, name='login-page'),
    path('logout-user', Logout, name='logout-user'),

    #Student Resources
    path('register-student', Register_Student, name='register-student'),
    path("view-students", Students_View, name='students'),  
    path('student-profile/<str:id>', Student_Profile, name='student-profile'),
    path("fprint-register/<str:id>", registerFingerPrint, name="fprint-register"),
    path('edit-student/<str:id>', editStudent, name='edit-student'),
    path('delete-student', deleteStudent, name='delete-student'),
    path('class-attendance', Class_Attendance, name='class-attandance'),
    path('class-attendance/<str:id>', Class_Attendance, name='class-attandance'),
    path('student-change-password/<str:id>', updatePasswordStudent, name='student-change-password'),


    #Staffs Resources
    path('staffs', Staffs_View, name='staffs' ),
    path('staff/<str:id>', Staff_Profile, name='staff-profile'),
    path('delete-staff', deleteStaff, name='delete-staff'),

    #Teachers Views
    path('lecturer-change-password', updatePasswordTeacher, name='lecturer-change-password'),
    path('lecturer-change-password/<str:id>', updatePasswordTeacher, name='lecturer-change-password'),
    path('lecturer-edit-credentials/<str:id>', editTeacher, name='lecturer-change-credentials'),
    path('lecturer-edit-credentials', editTeacher, name='lecturer-change-credentials'),
    path('register-teacher', addLecturer, name='register-teacher'),

    #Assuarer Views
    path('register-assuarer', addAssuarer, name='register-assuarer'),
    path('assuarer-change-password', updatePasswordAssuarer, name='assuarer-change-password'),
    path('assuarer-change-password/<str:id>', updatePasswordAssuarer, name='assuarer-change-password'),
    path('assuarer-edit-credentials/<str:id>', editAssuarer, name='assuarer-edit-credentials/'),
    path('assuarer-edit-credentials', editAssuarer, name='assuarer-edit-credentials/'),
    
    #Modules Manager
    path('modules', Modules_View, name='modules'),
    path('register-module', Create_Module, name='register-module'),
    path('edit-module/<str:id>', editModule, name='edit-module-view'),
    path('delete-module', deleteModule, name='delete-module'),

    #Device portals
    path("dev-fprint-portal", FPrintStudentReg.as_view(), name="device-fprint-portal"),
    path("dev-satt-portal", StudentAtt.as_view(), name="device-student-att-portal"),

    #Users App endpoint resources
    path('student-modules', GetStudentMondules.as_view(), name='student-modules'),
    path('student-attendance', GetStudentAttendance.as_view(), name='student-attendance'),
    path('login-student', AuthenticateStudent.as_view(), name='login-student')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

