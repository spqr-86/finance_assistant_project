from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    # path('', include('homepage.urls')),
    # path('about/', include('about.urls')),
    path('transactions/', include('transactions.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
