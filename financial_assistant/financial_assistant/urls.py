from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('homepage.urls')),
    # path('about/', include('about.urls')),
    path('transactions/', include('transactions.urls')),
    path('admin/', admin.site.urls),
]
