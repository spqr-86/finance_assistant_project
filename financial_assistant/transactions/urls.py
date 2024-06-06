from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path("", views.transactions_list, name='transactions_list'),
]
