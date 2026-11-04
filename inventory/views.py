from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView

from catalog.models import Variant

from .forms import MovementFilterForm, StockMovementForm
from .models import StockMovement
from .services import registrar_movimiento


class MovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = "inventory/movement_list.html"
    context_object_name = "movimientos"
    paginate_by = 20

    def get_queryset(self):
        queryset = StockMovement.objects.select_related(
            "variante__producto", "usuario"
        )
        self.filtro = MovementFilterForm(self.request.GET or None)

        if self.filtro.is_valid():
            datos = self.filtro.cleaned_data
            if datos["desde"]:
                queryset = queryset.filter(fecha__date__gte=datos["desde"])
            if datos["hasta"]:
                queryset = queryset.filter(fecha__date__lte=datos["hasta"])
            if datos["tipo"]:
                queryset = queryset.filter(tipo=datos["tipo"])
            if datos["producto"]:
                queryset = queryset.filter(variante__producto=datos["producto"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro"] = self.filtro
        context["filtros_activos"] = any(
            self.request.GET.get(campo)
            for campo in ("desde", "hasta", "tipo", "producto")
        )
        context["total_resultados"] = context["paginator"].count
        return context


class MovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = "inventory/movement_form.html"

    def get_initial(self):
        initial = super().get_initial()
        variante_id = self.request.GET.get("variante", "")
        if variante_id.isdigit():
            initial["variante"] = variante_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variante_id = self.request.GET.get("variante", "")
        if variante_id.isdigit():
            context["variante_seleccionada"] = (
                Variant.objects.filter(pk=variante_id)
                .select_related("producto")
                .first()
            )
        return context

    def form_valid(self, form):
        datos = form.cleaned_data
        try:
            movimiento = registrar_movimiento(
                variante=datos["variante"],
                tipo=datos["tipo"],
                cantidad=datos["cantidad"],
                nota=datos["nota"],
                usuario=self.request.user,
            )
        except ValidationError as error:
            # Normalmente el formulario ya validó; esto cubre errores de carrera.
            for campo, errores in getattr(error, "message_dict", {}).items():
                for mensaje in errores:
                    form.add_error(campo if campo in form.fields else None, mensaje)
            if not getattr(error, "message_dict", None):
                form.add_error(None, error)
            return self.form_invalid(form)

        messages.success(
            self.request,
            f"Movimiento registrado. Stock actual de la variante: "
            f"{movimiento.variante.stock_actual} unidades.",
        )
        return redirect("inventory:movement_list")
