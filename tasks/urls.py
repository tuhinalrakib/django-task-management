from django.urls import path
from tasks.views import dashboard, managerDashboard, employeeDashboard, test, task_create, show_task, update_task, delete_task, task_details

urlpatterns = [
    path("dashboard/", dashboard, name='dashboard'),
    path("manager-dashboard/", managerDashboard, name="manager-dashboard"),
    path("employee-dashboard/", employeeDashboard, name="user-dashboard"),
    path("test/", test),
    path("task-create/", task_create, name="task-create"),
    path("show-task/", show_task),
    path("task/<int:id>/details/", task_details, name= "task-details"),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
]