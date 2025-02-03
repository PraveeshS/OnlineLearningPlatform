from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import pyotp
from datetime import datetime, timedelta

from instructorDashboard.models import Instructor
from .models import Student
from .utils import send_otp  


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")  

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

         
            if Instructor.objects.filter(user=user).exists():
                return redirect("instructorHome")
            elif Student.objects.filter(user=user).exists():
                return redirect("home")
            else:
                messages.error(request, "Invalid role. Contact support.")
                return redirect("login")
        else:
            messages.error(request, "Incorrect username or password.")

    return render(request, "login.html")



def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["pass1"]
        password2 = request.POST["pass2"]
        role = request.POST["role"]


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

   
        request.session["signup_data"] = {
            "username": username,
            "email": email,
            "password": password1,
            "role": role
        }

   
        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret, interval=60)
        otp = totp.now()
        request.session["otp_secret"] = otp_secret
        request.session["otp_valid_until"] = (datetime.now() + timedelta(minutes=1)).isoformat()


        send_otp(email, otp)

        return redirect("otp")

    return render(request, "signup.html")



def otp_view(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        signup_data = request.session.get("signup_data")
        otp_secret = request.session.get("otp_secret")
        otp_valid_until = request.session.get("otp_valid_until")

        if not signup_data or not otp_secret or not otp_valid_until:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect("signup")

        valid_until = datetime.fromisoformat(otp_valid_until)

        if valid_until > datetime.now():
            totp = pyotp.TOTP(otp_secret, interval=60)

            if totp.verify(otp_entered, valid_window=1):
          
                user = User.objects.create_user(
                    username=signup_data["username"],
                    email=signup_data["email"],
                    password=signup_data["password"]
                )

      
                if signup_data["role"] == "student":
                    Student.objects.create(user=user)
                elif signup_data["role"] == "instructor":
                    Instructor.objects.create(user=user)

                login(request, user)

       
                request.session.pop("signup_data", None)
                request.session.pop("otp_secret", None)
                request.session.pop("otp_valid_until", None)

                messages.success(request, "Account created successfully!")
                return redirect("home" if signup_data["role"] == "student" else "instructorHome")

            else:
                messages.error(request, "Invalid OTP. Please try again.")
        else:
            messages.error(request, "OTP has expired. Request a new OTP.")

        return redirect("otp")

    return render(request, "otp.html")



def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")
