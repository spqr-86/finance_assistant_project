from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path('',
         views.TransactionListView.as_view(),
         name='list'),
    path('create/',
         views.TransactionCreateView.as_view(),
         name='create'),
    path('<int:pk>/edit/',
         views.TransactionUpdateView.as_view(),
         name='edit'
         ),
    path('<int:pk>/delete/',
         views.TransactionDeleteView.as_view(),
         name='delete'),
    path('dash/',
         views.dash,
         name='dash'),
    path('upload/',
         views.UploadPDFView.as_view(),
         name='upload_pdf')
]
