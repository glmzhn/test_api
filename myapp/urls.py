from django.urls import path
from .views import check_phone_number, verify_code, invite_user, get_invited_users

urlpatterns = [
    path('api/v1/check-phone/', check_phone_number, name='check-phone'),
    path('api/v1/verify-code/', verify_code, name='verify-code'),
    path('api/v1/invite-user/', invite_user, name='invite-user'),
    path('api/v1/get-invited-users/<str:unique_id>/', get_invited_users, name='get-invited-users'),
]
