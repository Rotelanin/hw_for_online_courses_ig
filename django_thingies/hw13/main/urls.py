from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("", views.product_list, name="product_list"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]
