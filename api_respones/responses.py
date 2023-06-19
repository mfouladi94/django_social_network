from django.http import JsonResponse , HttpResponse
from rest_framework.response import Response
from bson.json_util import dumps
'''
code : 100 success
code : 102 success with message and  data
       103 success with redirect
    
       200 success with data 

       400 error
       403 error with redirect

'''

response_struct = {
    'code': 100,
    'message': '',
    'errors': '',
    'next': "",
    'data': [],
}


def response_100_json_success_with_message(message):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 100
    return JsonResponse(body, status=200)


def response_102_json_success_with_message_data_field(message , data):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 102
    body['data'] = list()
    body['data'].append(data) 
    return JsonResponse(body, status=200)

def response_102_Response_with_json_body_success_with_message_data_field(message , data):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 102
    body['data'] = list()
    body['data'].append(data) 
    if isinstance(data, list):
        body['data'] = data
    
    return HttpResponse(dumps(body) ,content_type='application/json',status=200)



def response_103_json_success_with_message_redirect(message, link):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 103
    body['next'] = link
    return JsonResponse(body, status=200)


def response_400_json_error_with_message(message):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 400
    return JsonResponse(body, status=400)


def response_403_json_error_with_message_redirect(message, link):
    body = response_struct.copy()
    body['message'] = message
    body['code'] = 403
    body['next'] = link
    return JsonResponse(body, status=400)
