from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetails, Project
from datetime import date, timedelta
from django.db.models import Q,Count, Max, Min, Avg

# Create your views here.
def dashboard(request) :
    return render(request, "dashboard/dashboard.html")

def managerDashboard(request) :
    tasks = Task.objects.select_related("details").prefetch_related("assigned_to").all()

    #geting Task Count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status = "COMPLETED").count()
    # in_progress_task = Task.objects.filter(status = "INPROGRESS").count()
    # pending_task = Task.objects.filter(status = "PENDING").count()

    # count = {
    #     "total_task" : 
    #     "completed_task" :
    #     "in_progress_task" :
    #     "pending_task" :
    # }

    counts = Task.objects.aggregate(
        total = Count("id"),
        completed = Count("id", filter=Q(status = "COMPLETED")),
        in_progress = Count("id", filter=Q(status = "INPROGRESS")),
        pending_task = Count("id", filter=Q(status = "PENDING"))
    )

    context = {
        "tasks" : tasks,
        "counts" : counts,
    }

    return render(request, "dashboard/manager-dashboard.html",context)

def userDashboard(request) :
    return render(request, "dashboard/user-dashboard.html")

def test(request) :
    return render(request, "test.html")

def task_create(request) :
    # employees = Employee.objects.all()
    form = TaskModelForm () # get method

    # POST form 
    if request.method == "POST" :
        form = TaskModelForm(request.POST)
        if form.is_valid() :
            # --For Django ModelForm--
            form.save()
            return render(request, "task.html",{"form" : form, "message" : "task added successfully!"})

    context = {"form" : form}
    return render(request, "task.html" , context)

def show_task(request) : 
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    tasks = Task.objects.filter(due_date__lt = one_week_ago)

    return render(request, "show_task.html", 
                  {
                    "tasks" : tasks
                })