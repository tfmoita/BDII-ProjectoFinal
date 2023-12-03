from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor, PedidoCompracliente, FolhaDeObra
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm, PedidoCompraclienteForm, FolhaDeObraForm


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
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_cliente_read(%s, %s, %s, %s, %s, %s)",
                       [pk, '', '', '', 0 , ''])  # Preencha os valores vazios de acordo com seus dados
        row = cursor.fetchone()

        if row:
            cliente = {
                'nomecliente': row[0],
                'numerotelefonecliente': row[1],
                'email': row[2],
                'nif': row[3],
                'codigopostal': row[4]
            }
            return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})
        else:
            return render(request, 'cliente_not_found.html')


def cliente_create(request):
    form = ClienteForm()

    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.POST.get('nomecliente')
        telefone = request.POST.get('numerotelefonecliente')
        email = request.POST.get('email')
        nif = request.POST.get('nif')
        codigo_postal = request.POST.get('codigopostal')

        # Executar procedimento armazenado
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_cliente_create(%s, %s, %s, %s, %s)", [nome, telefone, email, nif, codigo_postal])

        # Atualizar a listagem de clientes após a criação do novo cliente
        clientes = Cliente.objects.all()  # Obter todos os clientes novamente

        return render(request, 'cliente/cliente_list.html', {'clientes': clientes})

    return render(request, 'cliente/cliente_form.html', {'form': form})


def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(instance=cliente)

    if request.method == 'POST':
        nome = request.POST.get('nomecliente')
        telefone = request.POST.get('numerotelefonecliente')
        email = request.POST.get('email')
        nif = request.POST.get('nif')
        codigo_postal = request.POST.get('codigopostal')

        with connection.cursor() as cursor:
            cursor.execute("CALL sp_cliente_update(%s, %s, %s, %s, %s, %s)", [pk, nome, telefone, email, nif, codigo_postal])

        return redirect('cliente_list')
    
    return render(request, 'cliente/cliente_form.html', {'form' : form, 'action' : 'Atualizar', 'cliente' : cliente})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_cliente_delete(%s), [pk]")

        return redirect('cliente_list')
    return render(request, 'cliente/cliente_confirm_delete.html', {'cliente' : cliente})

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

#Pedido compra a cliente view

def pedidocompracliente_list(request):
    pedidos = PedidoCompracliente.objects.all()
    return render(request, 'pedidocompracliente/pedidocompracliente_list.html', {'pedidos': pedidos})

def pedidocompracliente_detail(request, pk):
    pedido = get_object_or_404(PedidoCompracliente, pk=pk)
    return render(request, 'pedidocompracliente/pedidocompracliente_detail.html', {'pedido': pedido})

def pedidocompracliente_create(request):
    if request.method == 'POST':
        form = PedidoCompraclienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidocompracliente_list')
    else:
        form = PedidoCompraclienteForm()
    return render(request, 'pedidocompracliente/pedidocompracliente_form.html', {'form': form, 'action': 'Criar'})

def pedidocompracliente_update(request, pk):
    pedido = get_object_or_404(PedidoCompracliente, pk=pk)
    if request.method == 'POST':
        form = PedidoCompraclienteForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidocompracliente_list')
    else:
        form = PedidoCompraclienteForm(instance=pedido)
    return render(request, 'pedidocompracliente/pedidocompracliente_form.html', {'form': form, 'action': 'Atualizar', 'pedido': pedido})

def pedidocompracliente_delete(request, pk):
    pedido = get_object_or_404(PedidoCompracliente, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidocompracliente_list')
    return render(request, 'pedidocompracliente/pedidocompracliente_confirm_delete.html', {'pedido': pedido})

#folha de obra

def folha_de_obra_list(request):
    folha_de_obra = FolhaDeObra.objects.all()
    return render(request, 'folhadeobra/folha_de_obra_list.html', {'folhadeobra': folha_de_obra})

def folha_de_obra_detail(request, pk):
    folha_de_obra = get_object_or_404(FolhaDeObra, pk=pk)
    return render(request, 'folhadeobra/folha_de_obra_detail.html', {'folhadeobra': folha_de_obra})

def folha_de_obra_create(request):
    if request.method == 'POST':
        form = FolhaDeObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('folha_de_obra_list')
    else:
        form = FolhaDeObraForm()
    return render(request, 'folhadeobra/folha_de_obra_form.html', {'form': form, 'action': 'Criar'})

def folha_de_obra_update(request, pk):
    folha_de_obra = get_object_or_404(FolhaDeObra, pk=pk)
    if request.method == 'POST':
        form = FolhaDeObraForm(request.POST, instance=folha_de_obra)
        if form.is_valid():
            form.save()
            return redirect('folha_de_obra_list')
    else:
        form = FolhaDeObraForm(instance=folha_de_obra)
    return render(request, 'folha_de_obra/folha_de_obra_form.html', {'form': form, 'action': 'Atualizar', 'folha_de_obra': folha_de_obra})

def folha_de_obra_delete(request, pk):
    folha_de_obra = get_object_or_404(FolhaDeObra, pk=pk)
    if request.method == 'POST':
        folha_de_obra.delete()
        return redirect('folha_de_obra_list')
    return render(request, 'folha_de_obra/folha_de_obra_confirm_delete.html', {'folha_de_obra': folha_de_obra})