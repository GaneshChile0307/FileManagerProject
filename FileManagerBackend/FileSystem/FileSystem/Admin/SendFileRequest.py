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
from ..FileStore.blocklist import allCookies

Initial_URL = ' https://www.tu-chemnitz.de/informatik/DVS/blocklist/'
usercookies= allCookies


@csrf_exempt
def sendfilerequest(request):
    result={}
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        reqId = body['reqId']

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
        adminFileRequestsCollections=connection[db_name]['AdminFileRequest']

        fileRequestdetails = adminFileRequestsCollections.find_one({"reqID":int(reqId)})
        reqFileId= fileRequestdetails['fileID']
        reqStatus=fileRequestdetails['requestStatus']

        filedetails = FileUploadCollection.find_one({"fileId":int(reqFileId)})
        fileHash= filedetails['fileHash']
    
        if reqStatus=="block":
            res = requests.put(Initial_URL+str(fileHash), allow_redirects=False, cookies=usercookies)
            if res.status_code==201:
                result['msg']="File has been blocked successfully"
                result['status']='success'

                onID = { "fileId": int(reqFileId)}
                withValues={ "$set": { "fileStatus": reqStatus } }  
                FileUploadCollection.update_one(onID,withValues)

                return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                res['msg']="something wrong with file blocking"
                res['status']='failed'
                return HttpResponse(json.dumps(result),content_type="application/json")



        if reqStatus=="unblock":
            res = requests.delete(Initial_URL+str(fileHash), allow_redirects=False, cookies=usercookies)
            if res.status_code==204 :
                result['msg']="File has been unblocked successfully"
                result['status']='success'

                onID = { "fileId": int(reqFileId)}
                withValues={ "$set": { "fileStatus": reqStatus } }  
                FileUploadCollection.update_one(onID,withValues)

                return HttpResponse(json.dumps(result),content_type="application/json")
            
        else:
                res['msg']="something wrong with file blocking"
                result['status']='failed'
                return HttpResponse(json.dumps(result),content_type="application/json")

        myquery = { "reqID":reqId  }
        fileRequestdetails.delete_one(myquery)

    
    except Exception as ex :
        print(ex)
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
