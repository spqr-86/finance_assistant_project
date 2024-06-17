from django.contrib import admin
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    # path('', include('homepage.urls')),
    # path('about/', include('about.urls')),
    path('transactions/', include('transactions.urls')),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]


if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),) 