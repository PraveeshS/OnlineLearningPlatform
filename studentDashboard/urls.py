from os import stat
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [

    path('', views.studentHome, name='home'),
     path('offeredcourses', views.offeredcourses, name='offeredcourses'),
    path('course/<int:courseId>', views.course, name='course'),

    path("enrollCourse",views.enrollCourse , name="enrollCourse"),
    path('student/course/<int:course_id>/', views.student_course_detail, name='student_course_details'),
    path('content/<int:content_id>/', views.content1_detail, name='content1_detail'),
    path('delete_account/', views.delete_account, name='delete_account'),


  
]
     



if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)