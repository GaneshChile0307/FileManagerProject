from http import cookies
from http.cookiejar import CookieJar, CookiePolicy
from bs4 import BeautifulSoup
import requests


Initial_URL = ' https://www.tu-chemnitz.de/informatik/DVS/blocklist/'
UserName_URL = "https://wtc.tu-chemnitz.de/krb/module.php/TUC/username.php"
PassWord_URL = 'https://wtc.tu-chemnitz.de/krb/module.php/core/loginuserpass.php'
Saml2_Request_URL = " https://www.tu-chemnitz.de/Shibboleth.sso/SAML2/POST"



def blockProcess(URL='', method='', cookiess=None,  data=None, parse=None, parse_cond=None):
    anchorLink = ''

    if cookiess == None:
        cookie = {}
    else:
        cookie = {}
        cookie.update(cookiess)

    if method == "GET" and parse == None:
        res = requests.get(URL, allow_redirects=False, cookies=cookie)
        # print(res.status_code)
        return res.headers, res.cookies

    elif method == 'POST':
        res = requests.post(URL, allow_redirects=False,
                            data=data, cookies=cookie)
        # print(res.status_code)
        return res.headers, res.cookies

    elif method == "GET" and parse == True:

        if parse_cond == "reDirect":
            # print("parsing href link from anchor tag process starts")
            res = requests.get(URL, allow_redirects=False, cookies=cookie)
            soup = BeautifulSoup(res.content, 'html.parser')
            for link in soup.find_all('a'):
                anchorLink = link.get('href')
            headeLoc = anchorLink
            # print(res.status_code)
            return headeLoc, res.cookies

        elif parse_cond == "authState":
            # print("parsing href link from authstate  process starts")
            res = requests.get(URL, allow_redirects=False, cookies=cookie)
            soup = BeautifulSoup(res.content, 'html.parser')
            authValue = soup.find('input', {'name': 'AuthState'}).get('value')
            # print(res.status_code)
            return res.headers, res.cookies, authValue


def enterUserAndPassword(username=None, password=None, cookie=None, authState=None):

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    if username != None and password == None:
        # print("entered username")
        param = {"username": str(username), "AuthState": str(authState)}
        res = requests.post(UserName_URL, allow_redirects=False,
                            data=param, headers=headers, cookies=cookie)
        # print(res.status_code)
        return res.headers, res.cookies

    elif username == None and password != None:
        # print("entered password")
        param = {"password": str(password), "AuthState": str(authState)}
        res = requests.post(PassWord_URL, allow_redirects=False,
                            data=param, headers=headers, cookies=cookie)
        soup = BeautifulSoup(res.content, 'html.parser')
        # print(soup)
        samlRespose = soup.find('input', {'name': 'SAMLResponse'}).get('value')
        # print(res.status_code)
        return res.headers, res.cookies, samlRespose


def samlRequestProcess(cookie=None, saml_response=None):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    param = {"SAMLResponse": str(saml_response)}
    res = requests.post(Saml2_Request_URL, allow_redirects=False,
                        headers=headers,data=param, cookies=cookie)
    # print(res.status_code)
    return res.headers, res.cookies

def testBlockListWebService(cookie=None):
    res = requests.get(Initial_URL, allow_redirects=False, cookies=cookie)
    soup = BeautifulSoup(res.content, 'html.parser')
    # print(soup)
    # print(res.status_code)
    return res.headers, res.cookies

cks = {}
locationHeader_1, Ck = blockProcess(
    URL=Initial_URL, method='GET', cookiess=None)
# print("after location header 1")
# print(Ck.get_dict())


locationHeader_2, ck = blockProcess(
    URL=str(locationHeader_1['Location']), method='GET', cookiess=None)
# print("after location header 2")
cks.update(ck.get_dict())
# print(cks)

data = {"session": 'true',
        'user_idp': 'https://wtc.tu-chemnitz.de/shibboleth', "select": " "}
locationHeader_3, ck = blockProcess(
    URL=str(locationHeader_1['Location']), method='POST', cookiess=cks, data=data)
# print("after location header 3")
cks.update(ck.get_dict())
# print(cks)

locationHeader_4, ck = blockProcess(
    URL=str(locationHeader_3['Location']), method='GET', cookiess=cks)
# print("after location header 4")
cks.update(ck.get_dict())
# print(cks)


locationHeader_5, ck = blockProcess(URL=str(
    locationHeader_4['Location']), method='GET', cookiess=cks, parse=True, parse_cond="reDirect")
# print("after location header 5")
cks.update(ck.get_dict())
# print(cks)
# till here we get 401 status code


locationHeader_6, ck = blockProcess(
    URL=str(locationHeader_5), method='GET', cookiess=cks)
# print(locationHeader_6)
# print("after location header 6")
cks.update(ck.get_dict())
# print(cks)

locationHeader_7, ck, AuthState = blockProcess(URL=str(
    locationHeader_6['Location']), method='GET', cookiess=cks, parse=True, parse_cond="authState")
# print(locationHeader_7)
# print("after location header 7")
cks.update(ck.get_dict())
# print(cks)
# print(AuthState)

locationHeader_8, ck = enterUserAndPassword(
    username='chile', cookie=cks, authState=AuthState)
# print("after location header 8")
cks.update(ck.get_dict())
# print(cks)

locationHeader_9, ck = blockProcess(
    URL=str(locationHeader_8['Location']), method='GET', cookiess=cks)
# print(locationHeader_6)
# print("after location header 9")
cks.update(ck.get_dict())
# print(cks)


locationHeader_10, ck = blockProcess(
    URL=str(locationHeader_9['Location']), method='GET', cookiess=cks)
# print(locationHeader_6)
# print("after location header 9")
cks.update(ck.get_dict())
# print(cks)

locationHeader_11, ck, SamlResponse = enterUserAndPassword(
    password='xxxxxxxx', cookie=cks, authState=AuthState)
# print("after location header 11")
cks.update(ck.get_dict())
# print(cks)
# print(SamlResponse)

locationHeader_12, ck=samlRequestProcess(cookie=cks,saml_response=SamlResponse)
# print("after location header 12")
cks.update(ck.get_dict())
# print(cks)

locationHeader_13, ck = testBlockListWebService(cookie=cks)
# print("after location header 13")
cks.update(ck.get_dict())
# print(cks)  
allCookies=cks
# res = requests.get(Initial_URL+"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", allow_redirects=False, cookies=cks)
# print(res.status_code)