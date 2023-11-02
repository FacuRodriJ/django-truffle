from django import forms

from .models import DocumentoRendicion


class DocumentoRendicionForm(forms.ModelForm):
    """
    Formulario de Presentaciones
    """

    class Meta:
        model = DocumentoRendicion
        fields = ["archivo", "documento_requerido"]
        widgets = {
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
            "documento_requerido": forms.Select(attrs={"class": "form-select"}),
        }
