from django.test import TestCase



from django.test import Client
c = Client()
response = c.post('api-auth/login/', {'username':'test_user', 'password':'111'})
print(response.status_code)
payload = {"question_1":"sending some text on question 1...", "question_2":"text to question 2"}

#r = s.post("http://127.0.0.1:8000/survey_list/1/", data=payload, cookies=cookies)
#print(r.text)