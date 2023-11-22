from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraForm


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

def pedidocompra_create(request):
    if request.method == 'POST':
        form = PedidoCompraForm(request.POST)
        if form.is_valid():
            form.save()
            # Add any additional logic or redirection here
            return redirect('index')  # Adjust the URL name accordingly
    else:
        form = PedidoCompraForm()
    return render(request, 'pedidocompra/pedidocompra_form.html', {'form': form})


