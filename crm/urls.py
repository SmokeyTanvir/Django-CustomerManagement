from django.urls import path
from . import views

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
    path("deleteOrder/<str:orderID>", views.deleteOrder, name="deleteOrder")
]