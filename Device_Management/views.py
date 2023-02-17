from bson import json_util, ObjectId
import json
from Attendance_Management.MongoCRUD import AttendanceManager
#from pymongo import response
from Channels_Management.ChannelsManager import PostToRegisterChannel
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.views import APIView
from Mongo_DB.MongoDB import MongoDB

from Students_Management.MongoCRUD import MongoStudentsManager

class FPrintStudentReg(APIView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        data = {}
        data = request.data
        print(data)
        if not MongoStudentsManager().isStudent(data):
            x = f"{MongoDB().random_coll.insert_one({'data': 'rand'}).inserted_id}{MongoDB().random_coll.insert_one({'data': 'rand'}).inserted_id}" 
            v = f"{MongoDB().random_coll.insert_one({'data': 'rand'}).inserted_id}{MongoDB().random_coll.insert_one({'data': 'rand'}).inserted_id}"
            data['masked_print'] = x + v
            PostToRegisterChannel(data)

            return Response(True)
        return Response(False)

class StudentAtt(APIView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        data = request.data
        print(MongoStudentsManager().isStudent(data))
        if MongoStudentsManager().isStudent(data):
            print('hello')
            stud_data = MongoStudentsManager().getStudentData(data)
            att = AttendanceManager().attendClass(stud_data)
            return Response(att)

        return Response(False)