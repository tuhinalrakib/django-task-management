from django.urls import path
from users.views import sign_up, sign_in, signout, activate_user, admin_dashboard, assigned_role, CreateGroup, group_list

urlpatterns = [
    path("sign-up/", sign_up, name= "sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("logout/", signout, name="logout"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    
    path("admin/dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/<int:user_id>/assign-role/", assigned_role, name="assign-role"),
    path("admin/create-group/", CreateGroup, name="create-group"),
    path("admin/group-list/", group_list, name="group-list")
]
