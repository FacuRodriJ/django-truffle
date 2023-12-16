"""
URL configuration for django_setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import RendicionFormView, RendicionListView, RendicionDetailView, PresentacionDetailView
from validation.views import ValidacionView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(("core.urls", "core"), namespace="core")),
    path('rendiciones/', RendicionListView.as_view(), name='rendicion_list'),
    path('form-rendicion/<int:pk>/', RendicionFormView.as_view(), name='rendicion_form'),
    path('detalle-rendicion/<int:pk>/', RendicionDetailView.as_view(), name='rendicion_detail'),
    path('detalle-presentacion/<int:pk>/', PresentacionDetailView.as_view(), name='presentacion_detail'),
    path('validacion/', ValidacionView.as_view(), name="validacion_view")
    # path('validacion/', include(("validation.urls", "validation"), namespace="validacion")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
