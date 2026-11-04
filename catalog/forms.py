from django import forms

from .models import Product, Variant


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["nombre", "sku", "categoria", "marca", "precio", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej. Camisa Oxford"}),
            "sku": forms.TextInput(attrs={"placeholder": "Ej. CAM-OXF-001"}),
            "marca": forms.TextInput(attrs={"placeholder": "Opcional"}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def clean_sku(self):
        # Evita tener "abc-1" y "ABC-1" como productos distintos.
        return self.cleaned_data["sku"].strip().upper()


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ["talla", "color", "stock_minimo"]
        widgets = {
            "talla": forms.TextInput(attrs={"placeholder": "Ej. M"}),
            "color": forms.TextInput(attrs={"placeholder": "Ej. Azul"}),
            "stock_minimo": forms.NumberInput(attrs={"min": "0"}),
        }

    def __init__(self, *args, producto=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Asignamos el producto antes de validar para que la unicidad
        # (producto + talla + color) se compruebe correctamente.
        if producto is not None:
            self.instance.producto = producto

    def clean_talla(self):
        return self.cleaned_data["talla"].strip().upper()

    def clean_color(self):
        return self.cleaned_data["color"].strip().title()

    def clean(self):
        cleaned = super().clean()
        talla = cleaned.get("talla")
        color = cleaned.get("color")
        producto = self.instance.producto

        # Como `producto` no es un campo del formulario, Django no incluye la
        # restricción única en su validación automática: la comprobamos aquí.
        if producto and talla and color:
            existentes = Variant.objects.filter(
                producto=producto, talla=talla, color=color
            )
            if self.instance.pk:
                existentes = existentes.exclude(pk=self.instance.pk)
            if existentes.exists():
                raise forms.ValidationError(
                    "Ya existe una variante con esa talla y color para este producto."
                )
        return cleaned
