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
    path('equipamentos/<int:pk>/', views.equipamento_detail, name='equipamento_detail'),
    path('equipamentos/create/', views.equipamento_create, name='equipamento_create'),
    path('equipamentos/<int:pk>/update/', views.equipamento_update, name='equipamento_update'),
    path('equipamentos/<int:pk>/delete/', views.equipamento_delete, name='equipamento_delete'),

    path('componentes/', views.componente_list, name='componente_list'),
    path('componentes/<int:pk>/', views.componente_detail, name='componente_detail'),
    path('componentes/create/', views.componente_create, name='componente_create'),
    path('componentes/<int:pk>/update/', views.componente_update, name='componente_update'),
    path('componentes/<int:pk>/delete/', views.componente_delete, name='componente_delete'),

    path('pedidoscomprafornecedor/', views.pedidocomprafornecedor_list, name='pedidocomprafornecedor_list'),
    path('pedidoscomprafornecedor/<int:pk>/', views.pedidocomprafornecedor_detail, name='pedidocomprafornecedor_detail'),
    path('pedidoscomprafornecedor/create/', views.pedidocomprafornecedor_create, name='pedidocomprafornecedor_create'),
    path('pedidoscomprafornecedor/<int:pk>/update/', views.pedidocomprafornecedor_update, name='pedidocomprafornecedor_update'),
    path('pedidoscomprafornecedor/<int:pk>/delete/', views.pedidocomprafornecedor_delete, name='pedidocomprafornecedor_delete')
]
