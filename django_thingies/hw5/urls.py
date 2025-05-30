from django.urls import path
from .placeholder import admin_registration

urlpatterns = [
    path('admin/register/', admin_registration, name='admin_registration'),
]
