from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

from . import api


urlpatterns = [
    path('<int:page>/', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('<str:pk>/', api.post_detail, name='post_detail'),
    path('<str:pk>/like/', api.post_like, name='post_like'),
    path('<str:pk>/like/<int:page>/details/', api.post_like_detail, name='post_like_details'),
    path('<str:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<str:pk>/comment/<int:page>/replies/', api.post_get_comment_reply, name='post_get_comment_reply'),
    path('<str:pk>/comment/reply/', api.post_create_comment_reply, name='post_create_comment_reply'),
    path('<str:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/report/', api.post_report, name='post_report'),
    path('profile/<uuid:id>/<int:page>/', api.post_list_profile, name='post_list_profile'),



]