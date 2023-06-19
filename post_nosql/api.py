import math
from bson import ObjectId
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.files.storage import FileSystemStorage
import datetime
from bson.json_util import dumps
from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from api_respones.responses import *
from api_respones import messages
from django_social_network import settings

from .serializer import *
from .forms import PostForm, AttachmentForm
from .models import *


@api_view(['GET'])
def post_list(request, page=1):
    user_ids = [str(request.user.id)]

    for user in request.user.friends.all():
        print(str(user.id))
        user_ids.append(str(user.id))

    
    # query with pagination in posts 
    
    _query = {'created_by': {'$in': user_ids}}
    
    objects = Post.read_query_pagination(_query , offset=page)
    
    

    serializer = PostRetrieveSerializer(objects, many=True)
    data = serializer.get_serialized_data()
    
    response = {
        "currentPage": page,
        "data": data
    }
    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, response)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attach_id = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        # process the form data
        file = request.FILES['file']

        # save the file
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        attachment = Attatchment.construt(image=file_path, created_by=request.user.get_id_str())

        attach_id = attachment.create()

    if form.is_valid():

        attachs=list()
        if attach_id is not None:
            attachs.append(attach_id)
        
        post = Post.construt(body=form.cleaned_data['body'],
                             created_by=request.user.get_id_str(),
                             is_private=form.cleaned_data['is_private'],
                             attachments=attachs)

        answer_create_id = post.create()


        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, post.dump_to_dic())
    else:
        return response_400_json_error_with_message(messages.ErrorCreatePost+str(form.errors))


@api_view(['GET'])
def post_detail(request, pk):

    
    objects = Post.read_one(  {'_id': ObjectId(pk) , 'is_private': False}  )
    

    serializer = PostRetrieveSerializer(objects)
    data = serializer.get_serialized_data()

    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, data=data)


@api_view(['GET'])
def post_list_profile(request, id, page=1):
    user = User.objects.get(pk=id)
    str_user_id = str(id)

    are_friends = True
    if request.user not in user.friends.all():
        are_friends = False


    _query = {'created_by': str_user_id,
              '$or': [{'is_private': False}, {'is_private': are_friends} ] } 
    objects = Post.read_query_pagination(_query , offset=page)
    

    serializer = PostRetrieveSerializer(objects, many=True)
    data = serializer.get_serialized_data()

    user_serializer = UserSerializer(user)

    can_send_friendship_request = not are_friends


    check1 = FriendshipRequest.objects.filter(
        created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(
        created_for=user).filter(created_by=request.user)


    if check1 or check2:
        can_send_friendship_request = False

    response_data = {
        'postsContent': {
            "currentPage": page,
            'posts': data,
        },
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }
    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, data=response_data)


@api_view(['POST'])
def post_like(request, pk):
    user = request.user.id

    
    post_nosql = Post.read_one( {'_id': ObjectId(pk), 'is_private': False} )
    
    if post_nosql is None:
        return response_400_json_error_with_message(messages.POSTDOESNOTEXIST)
    
    post = Post()
    post.load_bson(post_nosql)


    liked = Like.read_one({'postID': pk, 'created_by': request.user.get_id_str()})

    if liked is None:
        like = Like.construt(created_by=request.user.get_id_str(), postID=pk)
        like = like.create()

        post.update_query({'$inc': {'likes_count': 1}})

        return response_100_json_success_with_message(messages.SUCCESSLIKE)
    else:
        liked_obj = Like()
        liked_obj.load_bson(liked)
        
        liked_obj.remove()
        post.update_query( {'$inc': {'likes_count': -1}} )
        

        return response_100_json_success_with_message(messages.ALREADYLIKED)


@api_view(['GET'])
def post_like_detail(request, pk, page=1):

    
    _query = {'postID': pk}
    objects_count = Like.read_all_pagination(offset=page)
    

    serializer = likeDetailSerilizer(objects_count, many=True)
    data = serializer.get_serialized_data()

    response = {
        "currentPage": page,
        "likes": data,
    }
    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, response)


@api_view(['POST'])
def post_create_comment(request, pk):
    body = request.data.get('body')

    if body is None or 1000 < len(body) < 25:
        return response_400_json_error_with_message(messages.ERRORLENGTHCOMMENT)

    
    _query = {'_id': ObjectId(pk), 'is_private': False} 
    post = Post.read_one(_query)
    
    if post is None:
        return response_400_json_error_with_message(messages.POSTDOESNOTEXIST)
        
    comment = Comment.construct(
        body=body, created_by=request.user.get_id_str(), postID=pk)
    comment_id = comment.create()

    postobj = Post()
    postobj.load_bson(post)
    
    postobj.add_comment(comment_id)
    postobj.update()

    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, comment.dump_to_dic())


@api_view(['POST'])
def post_create_comment_reply(request, pk):
    body = request.data.get('body')

    if body is None or 1000 < len(body) < 25:
        return response_400_json_error_with_message(messages.ERRORLENGTHCOMMENT)

    
    parent_comment = Comment.read_one({'_id': ObjectId(pk)})
    

    reply = Comment.construct(body=body, created_by=request.user.get_id_str(), postID=None, parentComment=pk)
    reply_id = reply.create()

    parent_comment['replies_count'] += 1
    parent_comment.update()

    serializer = CommentSerializer(reply)

    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, reply.dump_to_dic())


@api_view(['GET'])
def post_get_comment_reply(request, pk, page=1):


    _query = {'parentComment': pk}
    
    object_comment = Comment.read_query_pagination(_query , offset=page)
    
    serializer = CommentSerializer(object_comment, many=True)
    data = serializer.get_serialized_data()

    response = {
        "currentPage": page,
        "replies": data,
    }

    return response_102_Response_with_json_body_success_with_message_data_field(messages.SUCCESS, response)


@api_view(['DELETE'])
def post_delete(request, pk):

    
    objects = Post.remove_query({'created_by': request.user.get_id_str(), '_id': ObjectId(pk)})

    return response_100_json_success_with_message(messages.POSTDELETED)


@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return response_100_json_success_with_message(messages.POSTREPORTED)
