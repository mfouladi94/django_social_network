from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from api_respones import messages
from .forms import SignupForm
from .models import User, FriendshipRequest
from .serializers import *
from api_respones.responses import *


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
        user.is_active = True
        user.save()

        # TODO: send email for activation

        message = "success"
    else:
        success = False
        message = form.errors

    print(message)

    if not success:
        return response_400_json_error_with_message(message)
    return response_100_json_success_with_message(message)


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    # check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    check3 = user.friends.contains(request.user)

    if not check2 and not check3:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        return response_100_json_success_with_message(messages.FRIENDSHIPREQUESTCREATED)
    else:
        return response_400_json_error_with_message(messages.FRIENDSHIPREQUESTALREADYEXIST)


@api_view(['GET'])
def my_friendship_requests(request):
    user = request.user
    fr = FriendshipRequest.objects.filter(created_for=user, status=FriendshipRequest.SENT)

    serializer = FriendshipRequestSerializer(fr, many=True)

    return response_102_json_success_with_message_data_field(messages.SUCCESS, serializer.data)


@api_view(['GET'])
def requested_friendships(request):
    user = request.user
    fr = FriendshipRequest.objects.filter(created_by=user, status=FriendshipRequest.SENT)

    serializer = FriendshipRequestSerializer(fr, many=True)

    return response_102_json_success_with_message_data_field(messages.SUCCESS, serializer.data)


@api_view(['POST'])
def handle_request(request, pk, status):

    message = ""

    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(pk=pk)
    friendship_request.status = status
    friendship_request.save()

    if friendship_request.status == FriendshipRequest.ACCEPTED:
        request.user.friends.add(friendship_request.created_by)
        friendship_request.created_by.friends.add(request.user)
        
        request.user.friends_count += 1 
        friendship_request.created_by.friends_count +=1 
        
        request.user.save()
        friendship_request.created_by.save()
        
        

    elif friendship_request.status == FriendshipRequest.REJECTED:
        pass

    return response_100_json_success_with_message(messages.SUCCESS)


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)
