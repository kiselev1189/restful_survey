__author__ = 'kis'

import requests

s = requests.Session()
#s.auth = ('test_user', '111')
auth_r = s.post('http://127.0.0.1:8000/api-auth/login/?next=/survey_list/1/', {'username':'test_user', 'password':'123'})
#print(auth_r.text)
payload = {"question_1":"sending some text on question 1...", "question_2":"+999999"}

r = s.post("http://127.0.0.1:8000/survey_list/1/", data=payload)
print(r.text)