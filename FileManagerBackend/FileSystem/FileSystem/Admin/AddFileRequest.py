import hashlib
import os
from django.http import HttpResponse
import  pandas
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
import pymongo
from ..Configs.Config import config
from bson.timestamp import Timestamp
from datetime import datetime
from ..FileStore import hashPassword

@csrf_exempt
def AddFileRequestToAdmin(request):

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        userId = body['userId']   
        fileId = body['fileId']
        requestMessage = body['requestMessage']
        requestStatus= body['requestStatus']

    result={}
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")
        collection_name=params['collection_name'].replace("'", "")

        connection = MongoClient(mongodb_host, mongodb_port)
        collection = connection[db_name]['AdminFileRequest']  

        LastFileRequestData=collection.find().sort("reqID", -1).limit(1)
        for val in LastFileRequestData:
            prevReqID=val['reqID']
        currentReqId= prevReqID + 1

        timeStamp=datetime.now()
        
        collection.insert_one({"reqID":currentReqId,
                                "userID":userId,
                                "fileID":fileId,
                                 "requestMessage":requestMessage,
                                 "timeStamp":timeStamp,
                                 "requestStatus":requestStatus
                                })

        result['status']='success'
        result['msg']='User Registered Successfully'
        return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
