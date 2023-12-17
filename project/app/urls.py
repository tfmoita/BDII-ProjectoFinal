from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedor/<int:pk>/', views.fornecedor_detail, name='fornecedor_detail'),
    path('fornecedor/new/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedor/<int:pk>/update/', views.fornecedor_update, name='fornecedor_update'),
    path('fornecedor/<int:pk>/delete/', views.fornecedor_delete, name='fornecedor_delete'),

    path('clientes/', views.cliente_list, name='cliente_list'),
    path('cliente/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('cliente/create/', views.cliente_create, name='cliente_create'),
    path('cliente/<int:pk>/update/', views.cliente_update, name='cliente_update'),
    path('cliente/<int:pk>/delete/', views.cliente_delete, name='cliente_delete'),


    path('equipamentos/', views.equipamento_list, name='equipamento_list'),
    path('equipamento/<int:pk>/', views.equipamento_detail, name='equipamento_detail'),
    path('equipamento/create/', views.equipamento_create, name='equipamento_create'),
    path('equipamento/<int:pk>/update/', views.equipamento_update, name='equipamento_update'),
    path('equipamento/<int:pk>/delete/', views.equipamento_delete, name='equipamento_delete'),

    path('componentes/', views.componente_list, name='componente_list'),
    path('componente/<int:pk>/', views.componente_detail, name='componente_detail'),
    path('componente/create/', views.componente_create, name='componente_create'),
    path('componente/<int:pk>/update/', views.componente_update, name='componente_update'),
    path('componente/<int:pk>/delete/', views.componente_delete, name='componente_delete'),

    path('pedidoscomprafornecedor/', views.pedidocomprafornecedor_list, name='pedidocomprafornecedor_list'),
    path('pedidoscomprafornecedor/<int:pk>/', views.pedidocomprafornecedor_detail, name='pedidocomprafornecedor_detail'),
    path('pedidoscomprafornecedor/create/', views.pedidocomprafornecedor_create, name='pedidocomprafornecedor_create'),
    path('pedidoscomprafornecedor/<int:pk>/update/', views.pedidocomprafornecedor_update, name='pedidocomprafornecedor_update'),
    path('pedidoscomprafornecedor/<int:pk>/delete/', views.pedidocomprafornecedor_delete, name='pedidocomprafornecedor_delete'),

    path('pedidoscompracliente/', views.pedido_compracliente_list, name='pedido_compracliente_list'),
    path('pedidocompracliente/<int:pk>/', views.pedido_compracliente_detail, name='pedido_compracliente_detail'),
    path('pedidocompracliente/create/', views.pedido_compracliente_create, name='pedido_compracliente_create'),
    path('pedidocompracliente/<int:pk>/update/', views.pedido_compracliente_update, name='pedido_compracliente_update'),
    path('pedidocompracliente/<int:pk>/delete/', views.pedido_compracliente_delete, name='pedido_compracliente_delete'),

    path('folhas_de_obra/', views.folha_de_obra_list, name='folha_de_obra_list'),
    path('folhas_de_obra/<int:pk>/', views.folha_de_obra_detail, name='folha_de_obra_detail'),
    path('folhas_de_obra/create/', views.folha_de_obra_create, name='folha_de_obra_create'),
    path('folhas_de_obra/<int:pk>/update/', views.folha_de_obra_update, name='folha_de_obra_update'),
    path('folhas_de_obra/<int:pk>/delete/', views.folha_de_obra_delete, name='folha_de_obra_delete'),

    path('detalhespedidocompracliente/<int:pk>/', views.detalhes_pedidocompracliente_detail, name='detalhes_pedidocompracliente_detail'),
    path('detalhespedidocompracliente/create/', views.detalhes_pedidocompracliente_create, name='detalhes_pedidocompracliente_create'),
    path('detalhespedidocompracliente/<int:pk>/update/', views.detalhes_pedidocompracliente_update, name='detalhes_pedidocompracliente_update'),
    path('detalhespedidocompracliente/<int:pk>/delete/', views.detalhes_pedidocompracliente_delete, name='detalhes_pedidocompracliente_delete')
]
