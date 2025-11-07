from django.urls import path
from tasks.views import dashboard, managerDashboard, userDashboard, test, task_create, show_task, update_task, delete_task

urlpatterns = [
    path("dashboard/", dashboard),
    path("manager-dashboard/", managerDashboard, name="manager"),
    path("user-dashboard/", userDashboard),
    path("test/", test),
    path("task-create/", task_create, name="task-create"),
    path("show-task/", show_task),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
]