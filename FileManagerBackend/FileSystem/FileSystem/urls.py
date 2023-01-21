"""FileSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .UserAndAdmin import UserAPIs,RegisterUser

from .FileStore import uploadFile,retrieveFile

from .Admin import AddFileRequest, DeleteFileRequest , GetAdminFileRequest , SendFileRequest

from .Guest import CheckGuestTimer


# from django.contrib.auth import views as auth_views


urlpatterns = [

    path('UserLogin', UserAPIs.login_user, name="login_user"),
    path('Register', RegisterUser.register_user, name="register_user"),

    path('UploadFile', uploadFile.FileUploadView.as_view()),
    path('RetriveFile', retrieveFile.RetriveFile, name="RetriveFile"),

    path('GetUserById', UserAPIs.getUserByUserId, name="getUserByUserId"),
    path('GetUserFileDataByUserId', UserAPIs.getUserFileDataByUserId, name="getUserFileDataByUserId"),
    path('getAllUserFileData', UserAPIs.getAllUserFileData, name="getAllUserFileData"),
    path('deletefilerequestbyuser',UserAPIs.DeleteFileRequestFromUser , name="DeleteFileRequestFromUser"),
    
    path('AddFileRequestToAdmin',AddFileRequest.AddFileRequestToAdmin , name="AddFileRequestToAdmin"),
    path('deletefilerequest',DeleteFileRequest.DeleteFileRequestToAdmin , name="DeleteFileRequestToAdmin"),
    path('getalladminfilerequest',GetAdminFileRequest.GetAllAdminFileRequest , name="DeleteFileRequestToAdmin"),
    path('sendfilerequest',SendFileRequest.sendfilerequest , name="sendfilerequest"),

    path('guestchecktimer',CheckGuestTimer.CheckTimerForGuest , name="DeleteFileRequestToAdmin"),

]
