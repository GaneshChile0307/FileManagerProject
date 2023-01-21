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
import datetime as dt
from ..FileStore import hashPassword
from bson import json_util
from collections import defaultdict
import pandas


def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value
    return dict_obj

@csrf_exempt
def GetAllAdminFileRequest(request):
    print("inside request to admin")

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

        FileRequestcollection = connection[db_name]['AdminFileRequest']  
        userDetailsCollections=connection[db_name]['UserDetails']
        FileUploadCollection = connection[db_name]['FileUpload']  

        allFileRequestDetails=FileRequestcollection.find()
        print(allFileRequestDetails)
    
        reqData=[]
        for fq in allFileRequestDetails:
            userId= fq['userID']
            fileId = fq['fileID']

           
            userDetails = userDetailsCollections.find_one({"userID":userId})
            if userDetails:
                userDetails=userDetails
                userRegDate=userDetails['timeStamp']  
                uDate=userRegDate.strftime("%d-%m-%Y")
                userDetails['timeStamp']=uDate
                userDetails.pop('passWord')
            else:
                userDetails=None
            
            
            FileDetails = FileUploadCollection.find_one({"userID":fileId})
            if FileDetails:
                FileDetails=FileDetails
                fcd=FileDetails['filecreationDate']
                fud=FileDetails['fileUpdationDate']

                creatDate=fcd.strftime("%d-%m-%Y")
                updateDate=fud.strftime("%d-%m-%Y")

                FileDetails['filecreationDate']=creatDate
                FileDetails['fileUpdationDate']=updateDate

                FileDetails.pop('file_content')
            else:
                FileDetails=None

            fq['userDetails']=userDetails
            fq['FileDetails']=FileDetails
            reqData.append(fq)
        
        reqData =json_util.dumps(reqData)
        reqData=json.loads(reqData)
        df = pandas.DataFrame.from_records(reqData)
        js_data = df.to_json(orient = 'records')
        json_data =json.loads(js_data)

        result['status']='success'
        result['data']=json_data

        return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
