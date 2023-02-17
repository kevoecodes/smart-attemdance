import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util
from Attendance_Management.MongoCRUD import AttendanceManager

class GetStudentAttendance(APIView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        data = request.data
        attendance = AttendanceManager().studentWeekAttendance(data)

        return Response(json.loads(json_util.dumps(attendance)))


