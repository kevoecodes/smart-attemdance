from django.db import models

# Create your models here.


class Module(models.Model):
    modeule_code = models.CharField(max_length=200)
    module_name = models.CharField(max_length=200)
    lecturer_id = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)


class Attendance(models.Model):
    regNo = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    attendance_time = models.CharField(max_length=200)
    attendance_date = models.CharField(max_length=200)


class Staff(models.Model):
    firstname = models.CharField(max_length=200)
    staff_id = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    reg_at = models.CharField(max_length=200)
    staff_type = models.CharField(max_length=200)


class Student(models.Model):
    firstname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    regNo = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    reg_at = models.CharField(max_length=200)
    fprint_id = models.CharField(max_length=200)


class Timetable(models.Model):
    day = models.CharField(max_length=200)
    day_no = models.EmailField(max_length=200)
    module_code = models.CharField(max_length=200)
    _from = models.CharField(max_length=200)
    to = models.CharField(max_length=200)


