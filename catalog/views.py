from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from inventory.models import StockMovement

from .forms import ProductForm, VariantForm
from .models import Category, Product, Variant

# Reutilizamos esta consulta para que stock_total/stock_actual no hagan N+1.
VARIANTES_CON_MOVIMIENTOS = Prefetch(
    "variantes",
    queryset=Variant.objects.prefetch_related("movimientos").order_by("talla", "color"),
)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "productos"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("categoria")
            .prefetch_related(VARIANTES_CON_MOVIMIENTOS)
        )

        busqueda = self.request.GET.get("q", "").strip()
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda)
                | Q(sku__icontains=busqueda)
                | Q(marca__icontains=busqueda)
            )

        categoria = self.request.GET.get("categoria", "").strip()
        if categoria.isdigit():
            queryset = queryset.filter(categoria_id=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = self.request.GET.get("categoria", "").strip()
        context.update(
            {
                "categorias": Category.objects.all(),
                "busqueda": self.request.GET.get("q", "").strip(),
                "categoria_id": int(categoria) if categoria.isdigit() else None,
                "total_resultados": context["paginator"].count,
            }
        )
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "producto"

    def get_queryset(self):
        return Product.objects.select_related("categoria").prefetch_related(
            VARIANTES_CON_MOVIMIENTOS
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ultimos_movimientos"] = (
            StockMovement.objects.filter(variante__producto=self.object)
            .select_related("variante", "usuario")
            .order_by("-fecha", "-pk")[:8]
        )
        return context


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_message = "Producto creado correctamente."


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_message = "Producto actualizado correctamente."


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado.")
        return super().form_valid(form)


class VariantCreateView(LoginRequiredMixin, CreateView):
    model = Variant
    form_class = VariantForm
    template_name = "catalog/variant_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.producto = get_object_or_404(Product, pk=kwargs["product_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["producto"] = self.producto
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = self.producto
        context["es_edicion"] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, "Variante agregada al producto.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.producto.pk])


class VariantUpdateView(LoginRequiredMixin, UpdateView):
    model = Variant
    form_class = VariantForm
    template_name = "catalog/variant_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["producto"] = self.object.producto
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = self.object.producto
        context["es_edicion"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Variante actualizada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.object.producto_id])


class VariantDeleteView(LoginRequiredMixin, DeleteView):
    model = Variant
    template_name = "catalog/variant_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = self.object.producto
        return context

    def form_valid(self, form):
        messages.success(self.request, "Variante eliminada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.object.producto_id])
