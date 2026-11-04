from django import forms

from catalog.models import Product, Variant

from .models import StockMovement


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ["variante", "tipo", "cantidad", "nota"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"min": "0"}),
            "nota": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Opcional: proveedor, motivo del ajuste, etc.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostramos variantes de productos activos, con su producto
        # precargado para que el desplegable sea legible y eficiente.
        self.fields["variante"].queryset = (
            Variant.objects.filter(producto__activo=True)
            .select_related("producto")
            .order_by("producto__nombre", "talla", "color")
        )


class MovementFilterForm(forms.Form):
    """Filtros de la vista de historial (no guarda nada)."""

    desde = forms.DateField(
        label="Desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    hasta = forms.DateField(
        label="Hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    tipo = forms.ChoiceField(
        label="Tipo",
        required=False,
        choices=[("", "Todos"), *StockMovement.Tipo.choices],
    )
    producto = forms.ModelChoiceField(
        label="Producto",
        required=False,
        queryset=Product.objects.order_by("nombre"),
        empty_label="Todos los productos",
    )

    def clean(self):
        cleaned = super().clean()
        desde = cleaned.get("desde")
        hasta = cleaned.get("hasta")
        if desde and hasta and desde > hasta:
            raise forms.ValidationError("La fecha 'Desde' no puede ser posterior a 'Hasta'.")
        return cleaned
