from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import CuestomRegistrationForm, AssignedRoleForm, CreateGroupForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from users.forms import login_form
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch

# Create your views here.

# Test Users
def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def sign_up(request):
    if request.method == "GET":
        form = CuestomRegistrationForm()
    if request.method == "POST":
        form = CuestomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("passowrd1"))
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail sent. Please check your email")
            return redirect('sign-in')
        else:
            print("Password are not same")
    return render(request, "registration/register.html", {
        "form" : form
    })

def sign_in(request):
    form = login_form()
    if request.method == "POST":
        form = login_form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})

# @login_required
def signout(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id= user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User didn't found")

@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch("groups", queryset= Group.objects.all(), to_attr="all_groups")
        ).all()
    
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No group assigned"    
        
    return render(request, "admin/dashboard.html", {"users" : users})

@user_passes_test(is_admin, login_url="no-permission")
def assigned_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignedRoleForm
    if request.method == "POST":
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role");
            user.groups.clear() # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
    return render(request, "admin/assign_role.html", {"form" : form})
            
def CreateGroup(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} created successfully")
            return redirect("create-group")
        
    return render(request, "admin/create-group.html", {"form" : form})

def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(request, "admin/group_list.html", {"groups" : groups})