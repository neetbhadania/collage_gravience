from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import GrievanceForm
from .models import Grievance
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm


# Home Page
def viewdata(request):
    return render(request, "home.html")


# Grievance Form (login required)
@login_required
def grievance_form(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student_name = request.user.username  
            grievance.save()
            messages.success(request, "Grievance submitted successfully!")
            return redirect('viewdata') 
    else:
        form = GrievanceForm()
    return render(request, 'gravienceapp/student_grievance.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        admin_code = request.POST.get('admin_code', '').strip()
        if form.is_valid():
            user = form.save(commit=False)

           
            if admin_code and admin_code == getattr(settings, 'ADMIN_REG_CODE', ''):
                user.is_staff = True
                
                user.is_superuser = True

            user.save()

            # Auto-login after register
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
            
                if user.is_staff:
                    messages.success(request, "Registration successful — admin account created and logged in.")
                    return redirect('admin_grievances')
                else:
                    messages.success(request, "Registration successful — you are now logged in.")
                    return redirect('viewdata')
            else:
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                return redirect(next_url)

            if user.is_staff:
                return redirect("student_grievance")

            return redirect("student_grievance")

        messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('viewdata')   # this should be the name of your user_login URL'

@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, "Admin logged out.")
    return redirect('admin_login')   # URL name of admin login page'
# About Page
def about(request):
    return render(request, "about.html")

# Contact Page
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"""
        You have received a new message from your website contact form.

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        try:
            send_mail(
                subject=f"New Contact Message from {name}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['teacher@gmail.com'], 
            )

            send_mail(
                subject="Thanks for contacting us!",
                message=f"Hi {name},\n\nWe have received your message. We'll get back to you soon.\n\n– Student Grievance Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            messages.success(request, "Message sent successfully! A confirmation has been sent to your email.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect('contact')

    return render(request, 'contact.html')


# Delete grievance
def delete_grievance(request, id):
    grievance = get_object_or_404(Grievance, id=id)
    grievance.delete()
    messages.success(request, "Grievance deleted successfully.")
    return redirect('admin_grievances')

# Edit grievance
def edit_grievance(request, id):
    grievance = get_object_or_404(Grievance, id=id)
    if request.method == 'POST':
        grievance.student_name = request.POST.get('student_name')
        grievance.email = request.POST.get('email')
        grievance.subject = request.POST.get('subject')
        grievance.description = request.POST.get('description')
        grievance.save()
        messages.success(request, "Grievance updated successfully.")
        return redirect('admin_grievances')

    return render(request, 'edit_grievance.html', {'grievance': grievance})

def is_admin(user):
    return user.is_authenticated and user.is_staff

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def admin_login(request):
    # If already logged in as staff, send to admin page (or ?next= URL)
    if request.user.is_authenticated and request.user.is_staff:
        next_url = request.GET.get("next") or request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect('admin_grievances')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user.is_staff:  # only staff/admin allowed here
                login(request, user)

                # Respect ?next= if present
                next_url = request.GET.get("next") or request.POST.get("next")
                if next_url:
                    return redirect(next_url)

                return redirect('admin_grievances')
            else:
                messages.error(request, "You are not allowed to access the admin panel.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def admin_grievances(request):
    grievances = Grievance.objects.all().order_by('-created_at')

    total_grievances = grievances.count()
    today_grievances = grievances.filter(created_at__date=date.today()).count()

    context = {
        'grievances': grievances,
        'total_grievances': total_grievances,
        'today_grievances': today_grievances,
    }

    return render(request, 'admin_grievances.html', context)


# Admin-only check
def is_admin(user):
    return user.is_authenticated and user.is_staff


# Protect admin views with decorator
@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_grievances(request):
    grievances = Grievance.objects.all().order_by('-created_at')
    total_grievances = grievances.count()
    today_grievances = grievances.filter(created_at__date=date.today()).count()
    context = {
        'grievances': grievances,
        'total_grievances': total_grievances,
        'today_grievances': today_grievances,
    }
    return render(request, 'admin_grievances.html', context)



@login_required
@user_passes_test(is_admin, login_url='admin_login')
def delete_grievance(request, id):
    grievance = get_object_or_404(Grievance, id=id)
    grievance.delete()
    messages.success(request, "Grievance deleted successfully.")
    return redirect('admin_grievances')


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def edit_grievance(request, id):
    grievance = get_object_or_404(Grievance, id=id)
    if request.method == 'POST':
        grievance.student_name = request.POST.get('student_name')
        grievance.email = request.POST.get('email')
        grievance.subject = request.POST.get('subject')
        grievance.description = request.POST.get('description')
        grievance.save()
        messages.success(request, "Grievance updated successfully.")
        return redirect('admin_grievances')

    return render(request, 'edit_grievance.html', {'grievance': grievance})

from django.shortcuts import render
from django.http import HttpResponse


def viewdata(request):
    # students = students.objects.all() 
    return render(request,"home.html")                   

