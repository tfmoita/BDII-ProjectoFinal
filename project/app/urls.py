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

    path('armazens/', views.armazem_list, name='armazem_list'),
    path('armazem/<int:pk>/', views.armazem_detail, name='armazem_detail'),
    path('armazem/new/', views.armazem_create, name='armazem_create'),
    path('armazem/<int:pk>/update/', views.armazem_update, name='armazem_update'),
    path('armazem/<int:pk>/delete/', views.armazem_delete, name='armazem_delete'),

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
    path('componente/importar_componentes/', views.importar_componentes, name='importar_componentes'),

    path('pedidoscomprafornecedor/', views.pedido_comprafornecedor_list, name='pedido_comprafornecedor_list'),
    path('pedidoscomprafornecedor/<int:pk>/', views.pedido_comprafornecedor_detail, name='pedido_comprafornecedor_detail'),
    path('pedidoscomprafornecedor/create/', views.pedido_comprafornecedor_create, name='pedido_comprafornecedor_create'),
    path('pedidoscomprafornecedor/<int:pk>/delete/', views.pedido_comprafornecedor_delete, name='pedido_comprafornecedor_delete'),

    path('pedidoscompracliente/', views.pedido_compracliente_list, name='pedido_compracliente_list'),
    path('pedidocompracliente/<int:pk>/', views.pedido_compracliente_detail, name='pedido_compracliente_detail'),
    path('pedidocompracliente/create/', views.pedido_compracliente_create, name='pedido_compracliente_create'),
    path('pedidocompracliente/<int:pk>/update/', views.pedido_compracliente_update, name='pedido_compracliente_update'),
    path('pedidocompracliente/<int:pk>/delete/', views.pedido_compracliente_delete, name='pedido_compracliente_delete'),

    path('guiaremessafornecedor/', views.guia_remessafornecedor_list, name='guia_remessafornecedor_list'),
    path('guiaremessafornecedor/<int:pk>/', views.guia_remessafornecedor_detail, name='guia_remessafornecedor_detail'),
    path('guiaremessafornecedor/create/', views.guia_remessafornecedor_create, name='guia_remessafornecedor_create'),
    path('guiaremessafornecedor/<int:pk>/delete/', views.guia_remessafornecedor_delete, name='guia_remessafornecedor_delete'),

    path('guiaremessafcliente/', views.guia_remessacliente_list, name='guia_remessacliente_list'),
    path('guiaremessafcliente/<int:pk>/', views.guia_remessacliente_detail, name='guia_remessacliente_detail'),
    path('guiaremessafcliente/create/', views.guia_remessacliente_create, name='guia_remessacliente_create'),
    path('guiaremessafcliente/<int:pk>/delete/', views.guia_remessacliente_delete, name='guia_remessacliente_delete'),

    path('faturascliente/', views.faturacliente_list, name='faturacliente_list'),
    path('faturacliente/<int:pk>/', views.faturacliente_detail, name='faturacliente_detail'),
    path('faturacliente/create/', views.faturacliente_create, name='faturacliente_create'),
    path('faturacliente/<int:pk>/update/', views.faturacliente_update, name='faturacliente_update'),
    path('faturacliente/<int:pk>/delete/', views.faturacliente_delete, name='faturacliente_delete'),

    path('faturasfornecedor/', views.faturafornecedor_list, name='faturafornecedor_list'),
    path('faturafornecedor/<int:pk>/', views.faturafornecedor_detail, name='faturafornecedor_detail'),
    path('faturafornecedor/create/', views.faturafornecedor_create, name='faturafornecedor_create'),
    path('faturafornecedor/<int:pk>/update/', views.faturafornecedor_update, name='faturafornecedor_update'),
    path('faturafornecedor/<int:pk>/delete/', views.faturafornecedor_delete, name='faturafornecedor_delete'),

    path('folhadeobra/', views.folha_de_obra_list, name='folha_de_obra_list'),
    path('folhadeobra/<int:pk>/', views.folha_de_obra_detail, name='folha_de_obra_detail'),
    path('folhadeobra/create/', views.folha_de_obra_create, name='folha_de_obra_create'),
    path('folhadeobra/<int:pk>/delete/', views.folha_de_obra_delete, name='folha_de_obra_delete'),

    path('trabalhadores_operarios/', views.trabalhador_operario_list, name='trabalhador_operario_list'),
    path('trabalhador_operario/<int:pk>/', views.trabalhador_operario_detail, name='trabalhador_operario_detail'),
    path('trabalhador_operario/create/', views.trabalhador_operario_create, name='trabalhador_operario_create'),
    path('trabalhador_operario/<int:pk>/update/', views.trabalhador_operario_update, name='trabalhador_operario_update'),
    path('trabalhador_operario/<int:pk>/delete/', views.trabalhador_operario_delete, name='trabalhador_operario_delete'),

    path('mao_de_obra/', views.mao_de_obra_list, name='mao_de_obra_list'),
    path('mao_de_obra/<int:pk>/', views.mao_de_obra_detail, name='mao_de_obra_detail'),
    path('mao_de_obra/create/', views.mao_de_obra_create, name='mao_de_obra_create'),
    path('mao_de_obra/<int:pk>/update/', views.mao_de_obra_update, name='mao_de_obra_update'),
    path('mao_de_obra/<int:pk>/delete/', views.mao_de_obra_delete, name='mao_de_obra_delete'),

    path('exportar_pedidos_compra_json/', views.exportar_pedidos_compra_json, name='exportar_pedidos_compra_json'),

]
