from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

# Create your views here.
def dashboard(request) :
    return render(request, "dashboard/dashboard.html")

def managerDashboard(request) :
    return render(request, "dashboard/manager-dashboard.html")

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
            # --for Django Form Data---
            # data = form.cleaned_data
            # title = data.get("title")
            # descriptions = data.get('descriptions')
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to")
            # task = Task.objects.create(title=title,description=descriptions,due_date=due_date) 
            # # Assigned employee to Task
            # for emp_id in assigned_to :
            #     employee = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task Added Sucessfully")

    context = {"form" : form}
    return render(request, "task.html" , context)