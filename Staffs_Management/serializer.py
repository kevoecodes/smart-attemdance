from .models import Teacher
from rest_framework import serializers

class NewStaff(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('mobileNo', 'first_name', 'staff_id', 'last_name', 'gender', 'email')