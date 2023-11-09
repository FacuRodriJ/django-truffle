from django.urls import path

from .views import RendicionListView, RendicionFormView, RendicionDetailView, PresentacionDetailView, \
    ValidacionTemplateView

urlpatterns = [
    path('', RendicionListView.as_view(), name='rendicion_list'),
    path('form-rendicion/<int:pk>/', RendicionFormView.as_view(), name='rendicion_form'),
    path('detalle-rendicion/<int:pk>/', RendicionDetailView.as_view(), name='rendicion_detail'),
    path('detalle-presentacion/<int:pk>/', PresentacionDetailView.as_view(), name='presentacion_detail'),
    path('validacion/', ValidacionTemplateView.as_view(), name='validacion'),
]
