from django.contrib import admin

from instructorDashboard.models import Instructor
from .models import Student

admin.site.register(Student)
admin.site.register(Instructor)