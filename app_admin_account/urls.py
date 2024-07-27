from django.urls import path
from . import views



urlpatterns = [
    path("register/",views.user_register,name="register"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_logout,name="logout"),
    path("",views.dashboard, name='dashboard'),
    path('edit_profile/<int:user_id>/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name="change_password"),
    path('create_profile/<int:user_id>/',views.create_profile,name="create_profile"),
    path('my_order/',views.my_order,name='my_order'),
    path('view_order/<int:order_id>/',views.view_order,name='view_order'),
    path('delete_order/<int:order_id>/',views.delete_order,name='delete_order'),
    
]
