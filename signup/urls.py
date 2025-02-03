from django.urls import path
from . import views
urlpatterns = [

    path('', views.login_view, name='login'),
    path("logout_user",views.logout_user,name="logout"),
    path('signup/', views.sign_up , name = "signup"),
    path('otp',views.otp_view, name='otp')
]
