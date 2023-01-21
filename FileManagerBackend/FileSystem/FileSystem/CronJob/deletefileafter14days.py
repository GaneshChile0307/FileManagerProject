
from pymongo import MongoClient
import time
from Config import config
import sys
import os
from datetime import datetime


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
    fileDetails = FileUploadCollection.find({})   

    currentDate=datetime.now()

    # reqData=[]
    reqIdToDelete=[]
    for fq in fileDetails:
        fq.pop('file_content')
        fq.pop('fileHash')
        fud=fq['fileUpdationDate']
        updateDate=fud

        dayDifference = currentDate - updateDate
        dayDifference=dayDifference.days

        if dayDifference > 14:
           reqIdToDelete.append(fq['fileId']) 

    print(reqIdToDelete)
    if len(reqIdToDelete)>0:
        for fid in reqIdToDelete:
            FileUploadCollection.delete_one({"fileId":int(fid)})
            deletionTime=datetime.now().strftime("%H:%M %Y-%m-%d")
            with open('.test.txt', 'a+') as f:
                f.write("success in deleting file at "+ str(deletionTime)+" with id "+str(fid)+"\n")
    else: 
        with open('.test.txt', 'a+') as f:
                f.write("No file older than 14 days found in database \n")

except Exception as ex:
    print(ex)
    with open('.test.txt', 'a+') as f:
        f.write("error \n")

