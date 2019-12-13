
from django.urls import path
from .views import SignUpView, useractivateview
from django.contrib.auth.views import LoginView, LogoutView

loginpage ='myaccounts/login.html'
logoutpage = 'myaccounts/logout.html'

urlpatterns = [ 
    path('signup/',SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', useractivateview,name='activateuser'),
    path('login/',LoginView.as_view(template_name=loginpage),name='login'),
    path('logout/', LogoutView.as_view(template_name=logoutpage),name='logout'),
    #path('update/',StudentUpdate.as_view(), name='update'),
    #path('login/',StudentLogin.as_view(), name='login'),
    #path('logout/',StudentLogout.as_view(), name='logout'),
    #path('passwordChange/', StudentPchange.as_view(), name='passwdchange'),
    #path('passwordChangeDone/', StudentPchangeDone.as_view(), name='passwdchangedone')
]