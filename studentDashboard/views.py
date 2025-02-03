from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from signup.models import Instructor, Student
from instructorDashboard.models import Assignment,SubmittedAssignment,Course,Content, URLContent
from datetime import date,datetime
from django.db.models import Count




def studentHome(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:        
            return redirect("instructorHome")
        courses = student.courses.all()
        coursesInfo = []
        for c in courses:
            data = {
                "course":c,
                 "totalAssignments" : Assignment.objects.filter(course=c).count(),
                "submittedAssignments" : SubmittedAssignment.objects.filter(assignment__course=c, student=student).count()

            }
            coursesInfo.append(data)
    
    
        return render(request,"student/home.html",{
            "student":student,
            "coursesInfo": coursesInfo,
        
            })
    else:
        return redirect("login")


def offeredcourses(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:        
            return redirect("instructorHome")
        tag = request.GET.get('tag')
        sort = request.GET.get("sort_by")
        keyword = request.GET.get('search')
        courses = Course.objects.all()
        if tag:
            courses = courses.filter(tags__name=tag)
        if keyword:
            courses = courses.filter(title__icontains=keyword)
        match sort:
            case "price_low_high":
                courses = courses.order_by('price')
            case "price_high_low":
                courses = courses.order_by('-price')
            case "start_date_low_high":
                courses = courses.order_by('start_date')
            case "start_date_high_low":
                courses = courses.order_by('-start_date')

        return render(request, "student/offeredcourses.html", {
            "courses": courses,
        })
    else:
        return redirect("login")


def enrollCourse(request):
    if request.method == "POST":
        courseId = request.POST['courseId']
    else:
        return redirect('home')

    if request.user.is_authenticated:
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:        
            return redirect("instructorHome")
        course = Course.objects.filter(id=courseId).first()
        if course is None:
            return redirect("home")
        course_url = reverse('course', args=[courseId])

        if student in course.students.all():
            messages.success(request, "You are already enrolled in this course")
            return redirect(course_url)

        today = date.today()
        if course.start_date >= today:
            course.students.add(student)
            messages.success(request, "You have been enrolled in the course successfully.") 
            return redirect(course_url)

        messages.error(request, "The start date for this course has already passed, try enrolling when the next session starts.")
        return redirect(course_url)


def course(request, courseId):
    if request.user.is_authenticated:
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:        
            return redirect("instructorHome")
        
        course = Course.objects.filter(id=courseId).first()
        if course is None:
            return redirect("home")

        if student in course.students.all():
            return render(request, "student/courseEnrolled.html", {
                "course": course,
            })

        return render(request, "student/course.html", {
            "course": course,
        })
    else:
        return redirect("login")


def student_course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = Content.objects.filter(course=course)

    return render(request, 'student/course_details.html', {
        'course': course,
        'contents': contents,
    })







def student_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = Content.objects.filter(course=course)
    
    return render(request, 'student/course_details.html', {
        'course': course,
        'contents': contents,
    })



def content1_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    
    additional_contents = URLContent.objects.filter(content=content)


    return render(request, 'instructor/content1_detail.html', {
        'content': content,  
        'additional_contents': additional_contents  
    })



def content1_detail(request, content_id):
   
    content = get_object_or_404(Content, id=content_id)
    

    additional_contents = URLContent.objects.filter(content=content)

 
    return render(request, 'instructor/content_detail.html', {
        'content': content,  # 
        'additional_contents': additional_contents  
    })
    
    
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect("login")