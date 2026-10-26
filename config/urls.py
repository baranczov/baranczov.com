from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.root, name="root"),
    path("health/", views.health, name="health"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("<str:language>/", views.home, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

