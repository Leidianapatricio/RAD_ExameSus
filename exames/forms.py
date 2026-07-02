from django import forms
from .models import TipoExame


class TipoExameForm(forms.ModelForm):
    class Meta:
        model = TipoExame
        fields = ["nome", "descricao"]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Hemograma completo"
            }),
            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Descrição do tipo de exame"
            }),
        }