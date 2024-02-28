from django.urls import path
from .views import *
app_name = 'useracc'

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('register/', Register.as_view(), name='register'),
    path('email-verify/<str:uidb64>/<str:token>/', EmailVerify.as_view(), name='email_verify'),
    path('activate/<int:user_id>/', Activate.as_view(), name='activate'),
    path('delete_user/<int:user_id>/', DeleteUser.as_view(), name='delete_user'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('staff-page/', StaffPage.as_view(), name='staff_page'),
]
