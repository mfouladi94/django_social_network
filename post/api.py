from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .models import Post
from .serializers import *


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

