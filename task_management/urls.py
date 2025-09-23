from django.contrib import admin
from django.urls import path, include
from users.views import home,contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", home),
    path("contact/", contact),
    path("tasks/", include("tasks.urls"))
]
