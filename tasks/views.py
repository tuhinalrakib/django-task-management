from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailsForm
from tasks.models import Task, TaskDetails, Project
from datetime import date, timedelta
from django.db.models import Q,Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin

# Create your views here.

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_user(user):
    return user.groups.filter(name="User").exists()

# @user_passes_test(is_manager, login_url="no-permission")
def managerDashboard(request) :
    type = request.GET.get("type", "all")

    counts = Task.objects.aggregate(
        total = Count("id"),
        completed = Count("id", filter=Q(status = "COMPLETED")),
        in_progress = Count("id", filter=Q(status = "INPROGRESS")),
        pending_task = Count("id", filter=Q(status = "PENDING"))
    )

    # retrieve task Data
    base_query = Task.objects.select_related("details")

    if type == "completed" :
        tasks = base_query.filter(status = "COMPLETED")
    elif type == "in-progress" :
        tasks = base_query.filter(status = "INPROGRESS")
    elif type == "pending" :
        tasks = base_query.filter(status = "PENDING")
    elif type == "all" :
        tasks = base_query.all()

    context = {
        "tasks" : tasks,
        "counts" : counts,
    }

    return render(request, "dashboard/manager-dashboard.html",context)

# @user_passes_test(is_employee, login_url="no-permission")
def employeeDashboard(request) :
    return render(request, "dashboard/user-dashboard.html")

def test(request) :
    return render(request, "test.html")

# @login_required
# @permission_required("tasks.add_task", login_url="no-permission")
def task_create(request) :
    task_form = TaskModelForm () # get method
    task_details_form = TaskDetailsForm()

    # POST form 
    if request.method == "POST" :
        task_form = TaskModelForm (request.POST)
        task_details_form = TaskDetailsForm(request.POST, request.FILES)
        if task_form.is_valid() and task_details_form.is_valid() :
            # --For Django ModelForm--
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"Task Created Successfully")
            return redirect("task-create")

    context = {
        "task_form" : task_form,
        "task_details_form" : task_details_form
        }
    return render(request, "task.html" , context)

# @login_required
# @permission_required("tasks.change_task", login_url="no-permission")
def update_task(request, id) :
    task = Task.objects.get(id = id)
    task_form = TaskModelForm (instance=task) 
    if task.details :
        task_details_form = TaskDetailsForm(instance=task.details)
        

    # POST form 
    if request.method == "POST" :
        task_form = TaskModelForm (request.POST, instance = task)
        task_details_form = TaskDetailsForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_details_form.is_valid() :
            # --For Django ModelForm--
            task = task_form.save()
            task_detail = task_details_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"Task Update Successfully")
            return redirect("task-create")

    context = {
        "task_form" : task_form,
        "task_details_form" : task_details_form
        }
    return render(request, "task.html" , context)

# @login_required
# @permission_required("tasks.delete_task", login_url="no-permission")
def delete_task(request, id) : 
    if request.method == "POST" :
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect("manager")
    else :
        messages.success(request, "Success")
        return redirect("manager")

def show_task(request) : 
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    tasks = Task.objects.filter(due_date__lt = one_week_ago)

    return render(request, "show_task.html", 
                  {
                    "tasks" : tasks
                })

def task_details(request, id):
    task = Task.objects.get(id=id)
    status_choices = Task.STATUS_CHOICES
    
    if request.method == "POST":
        selected_status = request.POST.get("task_status")
        print(selected_status)
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)
        
    return render(request, "task_details.html", {
        "task": task,
        "status_choices" : status_choices
        })

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_user(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect("manager-dashboard")