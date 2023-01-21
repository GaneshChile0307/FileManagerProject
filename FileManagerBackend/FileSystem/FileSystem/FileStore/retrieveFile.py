from fileinput import filename
from time import sleep
from django import views
from django.http import HttpResponse
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
from io import BytesIO
from bson.timestamp import Timestamp
import datetime as dt
from datetime import datetime
import requests
from .blocklist import allCookies

Initial_URL = ' https://www.tu-chemnitz.de/informatik/DVS/blocklist/'
usercookies= allCookies


@csrf_exempt
def RetriveFile(request):
    result={}
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Id = body['id']
        fileId = body['fileId']

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")

        connection = MongoClient(mongodb_host, mongodb_port)

        FileUploadCollection = connection[db_name]['FileUpload']  
        userFileStatusCollection = connection[db_name]['UserFileStatus']  
        # userDetailsCollections=connection[db_name]['UserDetails']

        filedetails = FileUploadCollection.find_one({"fileId":int(fileId)})
        file_content= filedetails['file_content']
        filename=filedetails['filename']
        fileHash=filedetails['fileHash']
        
        res = requests.get(Initial_URL+str(fileHash), allow_redirects=False, cookies=usercookies)
       
        if res.status_code==200:
            with open('./'+filename, 'wb+') as temp_file:
                temp_file.write(file_content)
            
            newFileUpdateDate=datetime.now()

            onID = { "fileId": int(fileId)}
            withValues={ "$set": { "fileUpdationDate": newFileUpdateDate } }

            FileUploadCollection.update_one(onID,withValues)
        
            LastFileStatusData=userFileStatusCollection.find().sort("fileStatusID", -1).limit(1)
            for val in LastFileStatusData:
                prevFileStatusID=val['fileStatusID']
            currentFileStatusId= prevFileStatusID + 1


            downLoadDateTime= datetime.now()
            userFileStatusCollection.insert_one({"fileStatusID":currentFileStatusId, "fileID":fileId, "userEmail":Id , "fileDownloadTime":downLoadDateTime})

            if filedetails:
                result['status']='success'
                result['msg']='File Retrieved from database'
                return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                result['status']='failed'
                result['msg']='Something wrong with file retrival from database'
                return HttpResponse(json.dumps(result),content_type="application/json")

        elif res.status_code==210:
            result['status']='failed'
            result['msg']='File download access denied! Request Admin to unblock file'
            return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :
        print(ex)
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
