from django.contrib import admin
from .models import CategoriaMarmita, Marmita, Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


@admin.register(Marmita)
class MarmitaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'categoria',
        'preco_pequena',
        'preco_grande',
        'disponivel',
        'refrigerante'
    )

    search_fields = ('nome',)

    list_filter = (
        'categoria',
        'disponivel',
        'refrigerante'
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'cliente',
        'data',
        'status',
        'total'
    )

    search_fields = (
        'cliente__username',
    )

    list_filter = (
        'status',
        'data'
    )

    readonly_fields = ('data',)

    ordering = ('-data',)

    inlines = [ItemPedidoInline]


admin.site.register(CategoriaMarmita)
