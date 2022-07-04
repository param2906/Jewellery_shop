"""jewellery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("Contact/", views.contact, name="contactus"),
    path("bangles/", views.bangles, name="bangles"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("show_cart/", views.show_cart, name="show_cart"),
    path("liveprice/", views.get_price, name="liveprice"),
    path("appointment/", views.appointment, name="appointment"),
    path("feedback/", views.feedback, name="feedback"),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.paymentdone, name="paymentdone"),
    path("forgetpassword/", views.forgetpassword, name="forgetpassword"),
    path("changepassword/<token>/", views.changepassword, name="changepassword"),
    path("orders/", views.orders, name="orders"),
    path("view/", views.view, name="view"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
]

