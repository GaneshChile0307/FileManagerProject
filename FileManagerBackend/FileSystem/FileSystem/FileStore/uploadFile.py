from datetime import datetime
from time import sleep
from django import views
from django.http import HttpResponse
from numpy import byte
import  pandas
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from requests import Response
from ..Configs.Config import config
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import os
import base64, os
import bson
from pathlib import Path
import requests
from .blocklist import allCookies
from simple_file_checksum import get_checksum
from django.core.files.storage import FileSystemStorage

Initial_URL = ' https://www.tu-chemnitz.de/informatik/DVS/blocklist/'
usercookies= allCookies
# res = requests.get(Initial_URL+"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", allow_redirects=False, cookies=usercookies)
# print(res.status_code)


result={}
class FileUploadView(APIView):
    chunks=None
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        chunks=None
        try:
            file_data = request.FILES.getlist('file')
            userId=request.data['userid']

            # read connection parameters
            params = config()

             # connect to the PostgreSQL server
            print('Connecting to the MongoDB database...')

            mongodb_host=params['mongodb_host'].replace("'", "")
            mongodb_port=int(params['mongodb_port'])    
            db_name=params['db_name'].replace("'", "")


            connection = MongoClient(mongodb_host, mongodb_port)
            collection = connection[db_name]['FileUpload']

            
            for file in file_data:
               
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_path = fs.path(filename)
                print('absolute file path', uploaded_file_path)

                fileHash512=get_checksum(uploaded_file_path, algorithm="SHA256")

                size = os.path.getsize(uploaded_file_path)
                fileSize = str((int(size)/1024)/1024)

                for chunk in file.chunks():
                    pass
                    
                LastFileData=collection.find().sort("fileId", -1).limit(1)
                for val in LastFileData:
                    prevFileID=val['fileId']
                currentFileId= prevFileID + 1

                timeStamp=datetime.now()
                collection.insert_one({"filename":filename,
                                        "file_content":chunk,
                                        "fileId":int(currentFileId),
                                         "fileUpdationDate":timeStamp,
                                         "filecreationDate":timeStamp,
                                         "userID":int(userId),
                                         "fileStatus":"unblock",
                                         "fileSize":fileSize+" MB",
                                         "fileHash":fileHash512})
                

            result['status']='success'
            result['msg']='File Uploaded Successfully'
            return HttpResponse(json.dumps(result),content_type="application/json")


        except Exception as ex:
            print(ex)
            result['status']='failed'
            result['msg']=ex
            return HttpResponse(json.dumps(result),content_type="application/json")