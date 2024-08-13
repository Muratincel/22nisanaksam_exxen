from django.urls import path
from .views import *
from .views import delete_account

urlpatterns = [
    path('register/', userRegister, name="register"),
    path('login/', userLogin, name="userlogin"),
    path('logout/', userLogout, name="userlogout"),
    path('password_change/', passwordChange, name="password_change"),
    path('delete_account/', delete_account, name='delete_account'),
    path('account_delete/', accountDelete, name='account_delete'),

]