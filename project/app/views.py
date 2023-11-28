from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm


def index(request):
    return render(request, 'index.html')


# Fornecedor views:

def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedor/fornecedor_list.html', {'fornecedores': fornecedores})

def fornecedor_detail(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    return render(request, 'fornecedor/fornecedor_detail.html', {'fornecedor': fornecedor})

def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedor/fornecedor_form.html', {'form': form, 'action': 'Criar'})

def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'fornecedor/fornecedor_form.html', {'form': form, 'action': 'Editar'})

def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('fornecedor_list')
    return render(request, 'fornecedor/fornecedor_confirm_delete.html', {'fornecedor': fornecedor})

# Cliente views

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})

def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente/cliente_form.html', {'form': form, 'action': 'Criar'})

def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/cliente_form.html', {'form': form, 'action': 'Editar'})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'cliente/cliente_confirm_delete.html', {'cliente': cliente})

# Equipamento views

def equipamento_list(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'equipamento/equipamento_list.html', {'equipamentos': equipamentos})

def equipamento_detail(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    return render(request, 'equipamento/equipamento_detail.html', {'equipamento': equipamento})

def equipamento_create(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipamento_list')
    else:
        form = EquipamentoForm()
    return render(request, 'equipamento/equipamento_form.html', {'form': form, 'action': 'Criar'})

def equipamento_update(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('equipamento_list')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'equipamento/equipamento_form.html', {'form': form, 'action': 'Editar'})

def equipamento_delete(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        equipamento.delete()
        return redirect('equipamento_list')
    return render(request, 'equipamento/equipamento_confirm_delete.html', {'equipamento': equipamento})

#Componente view

def componente_list(request):
    componentes = Componente.objects.all()
    return render(request, 'componente/componente_list.html', {'componentes': componentes})

def componente_detail(request, pk):
    componente = get_object_or_404(Componente, pk=pk)
    return render(request, 'componente/componente_detail.html', {'componente': componente})

def componente_create(request):
    if request.method == 'POST':
        form = ComponenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('componente_list')
    else:
        form = ComponenteForm()
    return render(request, 'componente/componente_form.html', {'form': form, 'action': 'Criar'})

def componente_update(request, pk):
    componente = get_object_or_404(Componente, pk=pk)
    if request.method == 'POST':
        form = ComponenteForm(request.POST, instance=componente)
        if form.is_valid():
            form.save()
            return redirect('componente_list')
    else:
        form = ComponenteForm(instance=componente)
    return render(request, 'componente/componente_form.html', {'form': form, 'action': 'Editar', 'componente': componente})

def componente_delete(request, pk):
    componente = get_object_or_404(Componente, pk=pk)
    if request.method == 'POST':
        componente.delete()
        return redirect('componente_list')
    return render(request, 'componente/componente_confirm_delete.html', {'componente': componente})

#Pedido compra a fornecedor view


def pedidocomprafornecedor_list(request):
    pedidos = PedidoComprafornecedor.objects.all()
    return render(request, 'pedidocomprafornecedor/pedidocomprafornecedor_list.html', {'pedidos': pedidos})

def pedidocomprafornecedor_detail(request, pk):
    pedido = get_object_or_404(PedidoComprafornecedor, pk=pk)
    return render(request, 'pedidocomprafornecedor/pedidocomprafornecedor_detail.html', {'pedido': pedido})

def pedidocomprafornecedor_create(request):
    if request.method == 'POST':
        form = PedidoCompraFornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidocomprafornecedor_list')
    else:
        form = PedidoCompraFornecedorForm()
    return render(request, 'pedidocomprafornecedor/pedidocomprafornecedor_form.html', {'form': form, 'action': 'Criar'})

def pedidocomprafornecedor_update(request, pk):
    pedido = get_object_or_404(PedidoComprafornecedor, pk=pk)
    if request.method == 'POST':
        form = PedidoCompraFornecedorForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidocomprafornecedor_list')
    else:
        form = PedidoCompraFornecedorForm(instance=pedido)
    return render(request, 'pedidocomprafornecedor/pedidocomprafornecedor_form.html', {'form': form, 'action': 'Editar', 'pedido': pedido})

def pedidocomprafornecedor_delete(request, pk):
    pedido = get_object_or_404(PedidoComprafornecedor, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidocomprafornecedor_list')
    return render(request, 'pedidocomprafornecedor/pedidocomprafornecedor_confirm_delete.html', {'pedido': pedido})