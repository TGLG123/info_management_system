from django.urls import path

from records.views.user_management_views import user_management, add_user, delete_user, edit_user

urlpatterns = [
    #下面是用户管理
    path('users/', user_management, name='user_management'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/add/', add_user, name='add_user'),
]
