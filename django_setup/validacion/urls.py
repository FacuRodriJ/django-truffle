from django.urls import path

from .views import ValidacionView

urlpatterns = [
    path('', ValidacionView.as_view(), name="validacion")
]
