from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

from . import api


urlpatterns = [
    path('signup/', api.signup, name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]