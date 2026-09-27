from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    """Formulario del producto; reutiliza las validaciones del modelo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            )
            if self.is_bound and name in self.errors:
                field.widget.attrs["class"] += " is-invalid"
                field.widget.attrs["aria-invalid"] = "true"
                field.widget.attrs["aria-describedby"] = f"id_{name}_errors"

    class Meta:
        model = Producto
        fields = ("codigo", "nombre", "descripcion", "categoria", "precio", "stock")
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
            "codigo": forms.TextInput(attrs={"autofocus": True}),
            "precio": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"min": "0", "step": "1"}),
        }

    def clean_codigo(self):
        return self.cleaned_data["codigo"].strip()
