from django.contrib import admin
from .models import Cliente, CategoriaMarmita, Marmita, Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Marmita)
class MarmitaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel')
    search_fields = ('nome',)
    list_filter = ('categoria', 'disponivel')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data', 'status')
    search_fields = ('cliente__nome',)
    list_filter = ('status', 'data')
    readonly_fields = ('data',)
    ordering = ('-data',)
    inlines = [ItemPedidoInline]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email')
    search_fields = ('nome', 'email')


admin.site.register(CategoriaMarmita)