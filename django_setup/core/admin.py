from django.contrib import admin

from .models import Municipio, Rendicion, Presentacion, DocumentoRequerido

admin.site.register(Municipio)
admin.site.register(Rendicion)
admin.site.register(Presentacion)
admin.site.register(DocumentoRequerido)
