from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from api_respones.responses import *
from api_respones import messages
from django_social_network import settings
from .froms import PostForm, AttachmentForm

from .models import Post
from .serializers import *


@api_view(['GET'])
def post_list(request, page=1):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    # TODO: remove this .all , it's for test purposes
    posts = Post.objects.all()

    # pagination
    p = Paginator(posts, settings.DEFAULT_PER_PAGE)
    posts = p.page(page).object_list

    serializer = PostSerializer(posts, many=True)

    response = {
        "totalCount": p.count,
        "currentPage": page,
        "pages": p.num_pages,
        "data": serializer.data
    }
    return response_102_json_success_with_message_data_field(messages.SUCCESS, response)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    # TODO: commented this for test purposes if ui is available remove this line

    # if not attachment:
    #     return response_400_json_error_with_message(messages.ErrorCreatePostNoAttachment)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return response_102_json_success_with_message_data_field(messages.SUCCESS, serializer.data)
    else:
        return response_400_json_error_with_message(messages.ErrorCreatePost)


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return response_102_json_success_with_message_data_field(messages.SUCCESS , data={'post': PostDetailSerializer(post).data})



@api_view(['GET'])
def post_list_profile(request, id , page):

    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if request.user not in user.friends.all():
        posts = posts.filter(is_private=False)

    # pagination
    p = Paginator(posts, settings.DEFAULT_PER_PAGE)
    posts = p.page(page).object_list

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    data = {
        'postsContent': {
            "totalCount": p.count,
            "currentPage": page,
            "pages": p.num_pages,
            'posts' : posts_serializer.data,
        } ,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }
    return response_102_json_success_with_message_data_field(messages.SUCCESS, data=data)


@api_view(['POST'])
def post_like(request, pk):
    pass


@api_view(['POST'])
def post_create_comment(request, pk):
    pass


@api_view(['DELETE'])
def post_delete(request, pk):
    pass


@api_view(['POST'])
def post_report(request, pk):
    pass
