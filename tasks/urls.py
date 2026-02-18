from django.urls import path
from tasks.views import dashboard, managerDashboard, employeeDashboard, test, DeleteTask, Higreetings, CreateTask, TaskDetails, UpdateTask, ShowTask

urlpatterns = [
    path("dashboard/", dashboard, name='dashboard'),
    path("manager-dashboard/", managerDashboard, name="manager-dashboard"),
    path("employee-dashboard/", employeeDashboard, name="user-dashboard"),
    path("test/", test),
    path("task-create/", CreateTask.as_view(), name="task-create"),
    path("show-task/", ShowTask.as_view(), name="show-task"),
    path("task/<int:id>/details/", TaskDetails.as_view(), name= "task-details"),
    path("update-task/<int:id>/", UpdateTask.as_view(), name="update-task"),
    path("delete-task/<int:id>/", DeleteTask.as_view(), name="delete-task"),
    
    path("greetings/", Higreetings.as_view(), name="greetings")
]