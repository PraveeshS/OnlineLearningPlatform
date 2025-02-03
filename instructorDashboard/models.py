from django.db import models
from django.contrib.auth.models import User
from signup.models import Instructor, Student
from django.utils import timezone

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    start_date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subject = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag')
    students = models.ManyToManyField(Student, related_name='courses', blank=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='assignment_files')
    assigned_students = models.ManyToManyField(Student, through='AssignedAssignment', related_name='assigned_assignments')

    def __str__(self):
        return self.title

class AssignedAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Assignment: {self.assignment.title}, Student: {self.student.user.username}"

class SubmittedAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.TextField(null=True, blank=True)
    submission_file = models.FileField(upload_to='submission_files')

    def __str__(self):
        return f"Assignment: {self.assignment.title}, Student: {self.student.user.username}"

    class Meta:
        unique_together = ('student', 'assignment')

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class URLContent(models.Model):
    content = models.ForeignKey(Content, related_name='additional_contents', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=(('link', 'Link'), ('file', 'File')))

    def __str__(self):
        return self.title
