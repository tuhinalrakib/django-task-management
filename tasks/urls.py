from django.urls import path
from tasks.views import dashboard, managerDashboard, userDashboard, test, task_create

urlpatterns = [
    path("dashboard/", dashboard),
    path("manager-dashboard/", managerDashboard),
    path("user-dashboard/", userDashboard),
    path("test/", test),
    path("task-create/", task_create)
]