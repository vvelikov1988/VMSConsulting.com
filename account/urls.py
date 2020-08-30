from django.urls import path
from account.views import (
    index, profile,
    LOGIN, LOGOUT, REGISTER,
    activate, change_password, update_profile, change_profile_pic
)
from account.api import (
    check_username_existing, get_users
)

app_name = 'account'

urlpatterns = [
    # API URLs
    path('api/check_username/', check_username_existing, name='username_existing'),
    path('api/get_users/', get_users, name='get_users'),

    # View URLs
    path('', index, name='home'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('login/', LOGIN, name='login'),
    path('logout/', LOGOUT, name='logout'),
    path('register/', REGISTER, name='register'),
    path('update-password/', change_password, name='update-password'),
    path('update-profile/', update_profile, name='update-profile'),
    path('update-profile-pic', change_profile_pic, name='update-profile-pic'),

    # Functional URLs
    path('activate/<uidb64>/<token>', activate, name='activate'),


]