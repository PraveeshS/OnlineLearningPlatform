
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [

    path('', views.instructorHome, name='instructorHome'),
    path('newcourse', views.newCourse, name='newCourse'),
    path('course/<int:courseId>', views.courseDashboard, name='courseDashboard'),

    path('course/delete/<int:courseId>/', views.deleteCourse, name='deleteCourse'),
    path('course/update/<int:course_id>/', views.update_course, name='updateCourse'),
    path('course/<int:courseId>/addContent/', views.addContent, name='add_content'),
    path('content/<int:contentId>/update/', views.update_content, name='update_content'),
    path('content/<int:contentId>/delete/', views.deleteContent, name='delete_content'),

    path('content/<int:content_id>/add-url-content/', views.addURLContent, name='addURLcontent'),
    path('content/<int:content_id>/', views.content1_detail, name='content1_detail'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
     path('delete_account/', views.delete_account1, name='delete_account1'),
]
       





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)