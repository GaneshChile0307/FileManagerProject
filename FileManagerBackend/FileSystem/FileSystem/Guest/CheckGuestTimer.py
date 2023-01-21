import bson
from django import views
from django.http import HttpResponse
import  pandas
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
import pymongo
from requests import Response
from ..Configs.Config import config
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from io import BytesIO
from bson.timestamp import Timestamp
from datetime import datetime
from bson import json_util


@csrf_exempt
def CheckTimerForGuest(request):

    latestReId=None
    result={}
    id = request.GET.get('id')
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']   
        
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")
        

        connection = MongoClient(mongodb_host, mongodb_port)

        userFileStatusCollection = connection[db_name]['UserFileStatus']  

        if userFileStatusCollection.count_documents({ 'userEmail': id }, limit = 1):

            fileStatusDetails = userFileStatusCollection.find({"userEmail": id})

            print(fileStatusDetails)

            if fileStatusDetails ==None:
                print("in")
        
            if fileStatusDetails:
                for fsd in fileStatusDetails:
                    latestReId=fsd['fileStatusID']

                guestDetails = userFileStatusCollection.find_one({"fileStatusID": latestReId})
                fileDownLoadTime= guestDetails['fileDownloadTime']
                

                currentDateTime = datetime.now() 

                duration = currentDateTime - fileDownLoadTime
                duration_in_s = duration.total_seconds()
                minutes = divmod(duration_in_s, 60)[0]
                
                status=None
                if int(minutes)<10:
                    status=False
                else:
                    status=True

                if status:
                    result['status']='success'
                    result['msg']='Guest Is allowed to download a new file'
                    return HttpResponse(json.dumps(result),content_type="application/json")
                else:
                    result['status']='failed'
                    result['msg']='Access Denied , you cannot download until'
                    result['time']= 600 - int(duration_in_s)
                    return HttpResponse(json.dumps(result),content_type="application/json")

        else:

            result['status']='success'
            result['msg']='No previous record found ! you can dowmload bitch'
            return HttpResponse(json.dumps(result),content_type="application/json")


    except Exception as ex :

        print(ex)
        result['status']='failed'
        result['msg']=ex
        return HttpResponse(json.dumps(result),content_type="application/json")
