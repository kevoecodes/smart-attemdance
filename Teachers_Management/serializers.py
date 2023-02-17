from .models import Teacher
from rest_framework import serializers

class NewTeacher(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('mobileNo', 'first_name', 'lecturer_id', 'last_name', 'gender', 'email')