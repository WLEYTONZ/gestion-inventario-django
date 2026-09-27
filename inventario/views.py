from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoListView(ListView):
    """Muestra el inventario con su categoría asociada."""

    model = Producto
    template_name = "inventario/producto_list.html"
    context_object_name = "productos"
    queryset = Producto.objects.select_related("categoria")

    def get_queryset(self):
        queryset = super().get_queryset()
        consulta = self.request.GET.get("q", "").strip()
        if consulta:
            queryset = queryset.filter(codigo__icontains=consulta) | queryset.filter(
                nombre__icontains=consulta
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consulta"] = self.request.GET.get("q", "").strip()
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = "inventario/producto_detail.html"
    context_object_name = "producto"


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "inventario/producto_form.html"
    success_url = reverse_lazy("inventario:producto_lista")


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "inventario/producto_form.html"
    success_url = reverse_lazy("inventario:producto_lista")


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "inventario/producto_confirm_delete.html"
    context_object_name = "producto"
    success_url = reverse_lazy("inventario:producto_lista")
