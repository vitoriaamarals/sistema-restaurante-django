from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.home, 
        name='home'
    ),
    
    path(
        'marmitas/', 
        views.lista_marmitas, 
        name='marmitas'
    ),
    
    path(
        'pedidos/', 
        views.meus_pedidos, 
        name='pedidos'
    ),
    
    path(
        'cadastro/', 
        views.cadastro, 
        name='cadastro'
    ),
    
    path(
        'pedido/<int:marmita_id>/',
        views.criar_pedido,
        name='criar_pedido'
    ),
]

