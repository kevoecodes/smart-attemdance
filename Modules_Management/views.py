import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import json_util

from Modules_Management.MongoCRUD import MongoModulesManager
# Create your views here.

class GetStudentMondules(APIView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        data = request.data
        modules = MongoModulesManager().studentModules(data)

        return Response(json.loads(json_util.dumps(modules)))


    


