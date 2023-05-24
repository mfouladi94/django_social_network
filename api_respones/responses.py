from django.http import JsonResponse

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
    response_struct['message'] = message
    response_struct['code'] = 100
    return JsonResponse(response_struct, status=200)


def response_102_json_success_with_message_data_field(message , data):
    response_struct['message'] = message
    response_struct['code'] = 102
    response_struct['data'] = data
    return JsonResponse(response_struct, status=200)


def response_103_json_success_with_message_redirect(message, link):
    response_struct['message'] = message
    response_struct['code'] = 103
    response_struct['next'] = link
    return JsonResponse(response_struct, status=200)


def response_400_json_error_with_message(message):
    response_struct['message'] = message
    response_struct['code'] = 400
    return JsonResponse(response_struct, status=400)


def response_403_json_error_with_message_redirect(message, link):
    response_struct['message'] = message
    response_struct['code'] = 403
    response_struct['next'] = link
    return JsonResponse(response_struct, status=400)
