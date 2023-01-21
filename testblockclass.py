import blocklist
import requests
Initial_URL = ' https://www.tu-chemnitz.de/informatik/DVS/blocklist/'

usercookies= blocklist.allCookies
print(usercookies)

res = requests.get(Initial_URL+"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", allow_redirects=False, cookies=usercookies)
print(res.status_code)