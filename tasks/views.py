from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailsForm
from tasks.models import Task
from datetime import date, timedelta
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView

# variable fot list of decorators
create_decorators = [login_required, permission_required("tasks.add_task", login_url="no-permission")]

update_decorators = [login_required, permission_required("tasks.change_task", login_url="no-permission")]

delete_decorators = [login_required, permission_required("tasks.delete_task", login_url="no-permission")]

# Class Based Views Re-use Example
class Greetings(View):
    greeting = "Hello Every One"
    
    def get(self, request):
        return HttpResponse(self.greeting)

class Higreetings(Greetings):
    greeting = "Hi everyone"

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

class CreateTask(ContextMixin , LoginRequiredMixin , PermissionRequiredMixin,View):
    permission_required = "tasks.add_task"
    login_url = "sign-in"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_form"] = kwargs.get("task_form", TaskModelForm())
        context["task_details_form"] = kwargs.get("task_details_form", TaskDetailsForm())
        return context
    
    def get(self,request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, "task.html" , context)
    
    def post(self, request, *args, **kwargs):
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
                context = self.get_context_data(task_form= task_form, task_details_form=task_details_form)
                return render(request, "task.html" , context)

@method_decorator(update_decorators, name="dispatch")
class UpdateTask(View):
    def get(self,request, id, *args, **kwargs):
        task = Task.objects.get(id = id)
        task_form = TaskModelForm (instance=task) 
        if task.details :
            task_details_form = TaskDetailsForm(instance=task.details)
        
        context = {
        "task_form" : task_form,
        "task_details_form" : task_details_form
        }
        return render(request, "task.html" , context)
    
    def post(self,request, *args, **kwargs):
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

class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = "tasks.delete_task"
    login_url = "sign-in"
    path_name = "manager-dashboard"
    
    def get(self, request, *args, **kwargs):
        messages.success(request, "Success")
        return redirect(self.path_name)
    
    def post(self, request,id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        task.details.delete()
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect(self.path_name)

class ShowTask(View):
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    tasks = Task.objects.filter(due_date__lt = one_week_ago)
    
    def get(self, request, *args, **kwargs):
        return render(request, "show_task.html", 
                  {
                    "tasks" : self.tasks
                })

@method_decorator(login_required, name="dispatch")
class TaskDetails(View):    
    def get(self, request, id, *args, **kwargs):
        task = Task.objects.get(id=id)
        status_choices = Task.STATUS_CHOICES
        
        return render(request, "task_details.html", {
        "task": task,
        "status_choices" : status_choices
        })
        
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=id)
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_user(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect("manager-dashboard")