from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from .models import Content, Instructor, Course,  URLContent
from .models import Student
from .forms import ContentForm, CourseForm, URLContentForm



def instructorHome(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            instructor = Instructor.objects.get(user=user)
        except Instructor.DoesNotExist:        
            return redirect("home")

        courses = Course.objects.filter(instructor=instructor)
    

        return render(request, "instructor/home.html", {
            "instructor": instructor,
            "courses": courses,

        })
    else:
        return redirect("login")

# View for adding a new course
def newCourse(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            instructor = Instructor.objects.get(user=user)
        except Instructor.DoesNotExist:
            return redirect("login")

        if request.method == 'POST':
            form = CourseForm(request.POST, instructor=instructor)
            if form.is_valid():
                course = form.save()
                tags = form.cleaned_data.get('tags')
                if tags:
                    course.tags.set(tags)
                return redirect('instructorHome')
        else:
            form = CourseForm(instructor=instructor)

        return render(request, 'instructor/newCourse.html', {'form': form})
    else:
        return redirect("login")

# View for deleting a course
def deleteCourse(request, courseId):
    course = get_object_or_404(Course, id=courseId)
    if request.method == 'POST':
        course.delete()
        return redirect('instructorHome')
    return render(request, 'instructor/delete_course.html', {'course': course})


def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('instructorHome')
    else:
        form = CourseForm(instance=course)
    return render(request, 'instructor/update_course.html', {'form': form, 'course': course})

def addContent(request, courseId):
    if request.user.is_authenticated:
        user = request.user
        try:
            instructor = Instructor.objects.get(user=user)
        except Instructor.DoesNotExist:
            return redirect("login")

        course = get_object_or_404(Course, id=courseId, instructor=instructor)
        if request.method == 'POST':
            form = ContentForm(request.POST, request.FILES)
            if form.is_valid():
                content = form.save(commit=False)
                content.course = course
                content.save()
                messages.success(request, "Content added successfully!")
                return redirect('courseDashboard', courseId=course.id)
        else:
            form = ContentForm()

        return render(request, 'instructor/add_content.html', {
            'form': form,
            'course': course
        })
    else:
        return redirect("login")


def update_content(request, contentId):
    content = get_object_or_404(Content, id=contentId)
    course = content.course

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('courseDashboard', courseId=course.id)
    else:
        form = ContentForm(instance=content)

    return render(request, 'instructor/edit_content.html', {
        'form': form,
        'course': course
    })

def deleteContent(request, contentId):
    content = get_object_or_404(Content, id=contentId)
    course_id = content.course.id

    if request.method == 'POST':
        content.delete()
        return redirect('courseDashboard', courseId=course_id)

    return render(request, 'instructor/delete_content.html', {
        'content': content,
        'course': content.course
    })



def courseDashboard(request, courseId):
    if request.user.is_authenticated:
        user = request.user
        try:
            instructor = Instructor.objects.get(user=user)
        except Instructor.DoesNotExist:
            return redirect("login")

        course = get_object_or_404(Course, id=courseId)

        contents = Content.objects.filter(course=course)

        return render(request, 'instructor/course.html', {
            "course": course,
       
            "contents": contents,
       
        })
    else:
        return redirect("login")




def addURLContent(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    
    if request.method == 'POST':
        form = URLContentForm(request.POST, request.FILES)
        if form.is_valid():
            url_content = form.save(commit=False)
            url_content.content = content
            
            if url_content.content_type == 'link':
                url_content.file = None 
            elif url_content.content_type == 'file':
                url_content.url = ''  
            
            url_content.save()
            return redirect('content1_detail', content_id=content.id)
    else:
        form = URLContentForm()
    
    return render(request, 'instructor/add_url_content.html', {
        'form': form,
        'content': content,
    })





def content1_detail(request, content_id):

    content = get_object_or_404(Content, id=content_id)
    
    additional_contents = URLContent.objects.filter(content=content)


    return render(request, 'instructor/content_detail.html', {
        'content': content,  
        'additional_contents': additional_contents  
    })


from django.http import FileResponse, Http404
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import URLContent

def download_file(request, file_id):
    content = get_object_or_404(URLContent, id=file_id)

    if not content.file:
        raise Http404("File not found")

    file_path = content.file.path  # Get the file path from the model
    file_name = os.path.basename(file_path)  # Get the original file name

    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response


def delete_account1(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect("login")