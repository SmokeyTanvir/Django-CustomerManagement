from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),

    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),

    path("products/", views.products, name="products"),
    path("customer/<int:customerID>", views.customer, name="customer"),
    path("user/", views.user_page, name="user_page"),
    path("account/", views.accountSettings, name="account"),
    
    path("create_order/<str:pk>", views.create_order, name="create_order"),
    path("updateOrder/<str:orderID>", views.updateOrder, name="updateOrder"),
    path("deleteOrder/<str:orderID>", views.deleteOrder, name="deleteOrder"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="crm/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="crm/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="crm/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="crm/password_reset_complete.html"), name="password_reset_complete"),
]