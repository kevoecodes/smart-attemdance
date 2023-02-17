from .models import Student
from rest_framework import serializers

class NewStudent(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('regNo', 'first_name', 'last_name', 'gender', 'email')