from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm
from .models import User
from api_respones.responses import response_100_json_success_with_message, response_400_json_error_with_message


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    success = True

    form = SignupForm({
        'email': data.get('email'),
        'username': data.get('username'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        # TODO: send email for activation

        message = "success"
    else:
        success = False
        message = form.errors

    print(message)

    if not success :
        return response_400_json_error_with_message(message)
    return response_100_json_success_with_message(message)
