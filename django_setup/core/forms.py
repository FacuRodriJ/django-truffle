from django import forms

from .models import Documento


class DocumentoForm(forms.ModelForm):
    """
    Formulario de Presentaciones
    """

    class Meta:
        model = Documento
        fields = ["archivo", "documento_requerido"]
        widgets = {
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
            "documento_requerido": forms.Select(attrs={"class": "form-select"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.fields['documento_requerido'].empty_label = "Seleccione una opción"
