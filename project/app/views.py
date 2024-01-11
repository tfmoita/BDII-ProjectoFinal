from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor, PedidoCompracliente, FolhaDeObra, DetalhesPedidocompracliente
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm, FolhaDeObraForm, PedidoDetalhesForm
from datetime import datetime

def index(request):
    return render(request, 'index.html')
 

# Fornecedor views:

def fornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_fornecedor()')
        columns = [col[0] for col in cursor.description]
        fornecedores = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'fornecedor/fornecedor_list.html', {'fornecedores': fornecedores})

def fornecedor_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_fornecedor_read(%s, %s, %s, %s, %s)", [pk, '', '', '', ''])  
        row = cursor.fetchone()

        if row:
            fornecedor = {
                'nomefornecedor': row[0],
                'email': row[1],
                'numerotelefonefornecedor': row[2],
                'codigopostal': row[3],
                'idfornecedor': pk
            }
            return render(request, 'fornecedor/fornecedor_detail.html', {'fornecedor': fornecedor})

        raise Http404("Fornecedor does not exist")

def fornecedor_create(request):
    form = FornecedorForm()

    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_fornecedor_create(%s, %s, %s, %s)", [data['nomefornecedor'], data['email'], data['numerotelefonefornecedor'], data['codigopostal']])
            return redirect('fornecedor_list')

    return render(request, 'fornecedor/fornecedor_form.html', {'form': form})

def fornecedor_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_fornecedor_read(%s, %s, %s, %s, %s)", [pk, '', '', '', ''])
            row = cursor.fetchone()

            if row:
                fornecedor_data = {
                    'nomefornecedor': row[0],
                    'email': row[1],
                    'numerotelefonefornecedor': row[2],
                    'codigopostal': row[3],
                }
                form = FornecedorForm(initial=fornecedor_data)

                if request.method == 'POST':
                    form = FornecedorForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_fornecedor_update(%s, %s, %s, %s, %s)", [pk, data['nomefornecedor'], data['email'], data['numerotelefonefornecedor'], data['codigopostal']])
                        return redirect('fornecedor_list')
                else:
                    return render(request, 'fornecedor/fornecedor_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

def fornecedor_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_fornecedor_read(%s, %s, %s, %s, %s)", [pk, '', '', '', ''])
            row = cursor.fetchone()

            if row:
                fornecedor = get_object_or_404(Fornecedor, pk=pk)
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_fornecedor_delete(%s)", [pk])
                    return redirect('fornecedor_list')
                else:
                    return render(request, 'fornecedor/fornecedor_confirm_delete.html', {'fornecedor': fornecedor})
            else:
                raise Http404("Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")


# Cliente views

def cliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_cliente()')
        columns = [col[0] for col in cursor.description]
        clientes = [dict(zip(columns, row)) for row in cursor.fetchall()]

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
                'codigopostal': row[4],
                'idcliente': pk
            }
            return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})
        
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
    # Recupere os dados do cliente usando a conexão ou ORM do Django

    try:
        # Recupere os dados do cliente
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_cliente_read(%s, %s, %s, %s, %s, %s)", [pk, '', '', '', 0, ''])
            row = cursor.fetchone()

            if row:
                cliente_data = {
                    'nomecliente': row[0],
                    'numerotelefonecliente': row[1],
                    'email': row[2],
                    'nif': row[3],
                    'codigopostal': row[4]
                }
                # Inicialize o formulário com os dados do cliente
                form = ClienteForm(initial=cliente_data)

                if request.method == 'POST':
                    # Atualize o formulário com os dados recebidos
                    form = ClienteForm(request.POST)
                    if form.is_valid():
                        # Se o formulário for válido, atualize os dados no banco
                        data = form.cleaned_data
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_cliente_update(%s, %s, %s, %s, %s, %s)",
                                           [pk, data['nomecliente'], data['numerotelefonecliente'],
                                            data['email'], data['nif'], data['codigopostal']])
                        return redirect('cliente_list')
                else:
                    # Se for uma requisição GET, renderize o formulário
                    return render(request, 'cliente/cliente_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Cliente does not exist")

    except Exception as e:
        # Lide com exceções conforme necessário
        print(e)  # Apenas para depuração, você pode usar um logger aqui
        raise Http404("Erro ao processar a solicitação")

def cliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            # Verifica se o cliente existe
            cursor.execute("CALL sp_cliente_read(%s, %s, %s, %s, %s, %s)", [pk, '', '', '', 0, ''])
            row = cursor.fetchone()

            if row:
                cliente = Cliente.objects.get(pk=pk)  # Recupera o objeto Cliente a ser deletado

                if request.method == 'POST':
                    # Executa o procedimento armazenado para deletar o cliente
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_cliente_delete(%s)", [pk])
                    
                    return redirect('cliente_list')
                else:
                    # Se for uma requisição GET, renderiza a confirmação de exclusão
                    return render(request, 'cliente/cliente_confirm_delete.html', {'cliente': cliente})
            else:
                raise Http404("Cliente does not exist")

    except Exception as e:
        print(e)  # Log do erro para depuração
        raise Http404("Erro ao processar a solicitação")


# Equipamento views

def equipamento_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_equipamento()')
        columns = [col[0] for col in cursor.description]
        equipamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'equipamento/equipamento_list.html', {'equipamentos': equipamentos})

def equipamento_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_equipamento_read(%s, %s, %s)", [pk, '', ''])  # Ajuste conforme necessário
        row = cursor.fetchone()

        if row:
            equipamento = {
                'nomeequipamento': row[0],
                'descricao': row[1],
                'idequipamento': pk
                # Adicione outros campos conforme necessário
            }
            return render(request, 'equipamento/equipamento_detail.html', {'equipamento': equipamento})

        raise Http404("Equipamento does not exist")

def equipamento_create(request):
    form = EquipamentoForm()

    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_equipamento_create(%s, %s)", [data['nomeequipamento'], data['descricao']])
            return redirect('equipamento_list')

    return render(request, 'equipamento/equipamento_form.html', {'form': form})

def equipamento_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_equipamento_read(%s, %s, %s)", [pk, '', ''])
            row = cursor.fetchone()

            if row:
                equipamento_data = {
                    'nomeequipamento': row[0],
                    'descricao': row[1],
                    # Adicione outros campos conforme necessário
                }
                form = EquipamentoForm(initial=equipamento_data)

                if request.method == 'POST':
                    form = EquipamentoForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        
                        # Execute este procedimento para verificar a passagem de valores
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_equipamento_update(%s, %s, %s)", [pk, data['nomeequipamento'], data['descricao']])
                        return redirect('equipamento_list')
                else:
                    return render(request, 'equipamento/equipamento_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Equipamento does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

def equipamento_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_equipamento_read(%s, %s, %s)", [pk, '', ''])
            row = cursor.fetchone()

            if row:
                equipamento = get_object_or_404(Equipamento, pk=pk)
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_equipamento_delete(%s)", [pk])
                    return redirect('equipamento_list')
                else:
                    return render(request, 'equipamento/equipamento_confirm_delete.html', {'equipamento': equipamento})
            else:
                raise Http404("Equipamento does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

#Componente view

def componente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_componente()')
        columns = [col[0] for col in cursor.description]
        componentes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'componente/componente_list.html', {'componentes': componentes})

def componente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_componente_read(%s, %s)", [pk, ''])  # Ajuste conforme necessário
        row = cursor.fetchone()

        if row:
            componente = {
                'nomecomponente': row[0],
                'idcomponente': pk
                # Adicione outros campos conforme necessário
            }
            return render(request, 'componente/componente_detail.html', {'componente': componente})

        raise Http404("Componente does not exist")

def componente_create(request):
    form = ComponenteForm()

    if request.method == 'POST':
        form = ComponenteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_componente_create(%s)", [data['nomecomponente']])
            return redirect('componente_list')

    return render(request, 'componente/componente_form.html', {'form': form})

def componente_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_componente_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                componente_data = {
                    'nomecomponente': row[0]
                    # Adicione outros campos conforme necessário
                }
                form = ComponenteForm(initial=componente_data)

                if request.method == 'POST':
                    form = ComponenteForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        print("Valor de pk:", pk)
                        print("Valor de data['nomecomponente']:", data['nomecomponente'])  # Verifica o valor de 'nomecomponente'
                        
                        # Execute este procedimento para verificar a passagem de valores
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_componente_update(%s, %s)", [pk, data['nomecomponente']])
                        return redirect('componente_list')
                else:
                    return render(request, 'componente/componente_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Componente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

def componente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_componente_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                componente = get_object_or_404(Componente, pk=pk)
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_componente_delete(%s)", [pk])
                    return redirect('componente_list')
                else:
                    return render(request, 'componente/componente_confirm_delete.html', {'componente': componente})
            else:
                raise Http404("Componente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")


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

def pedido_compracliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_pedido_compracliente()')
        columns = [col[0] for col in cursor.description]
        pedidos_compra_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_compracliente/pedido_compracliente_list.html', {'pedidos_compra_cliente': pedidos_compra_cliente})

def pedido_compracliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_pedido_compracliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])  
        row = cursor.fetchone()

        if row:
            idcliente = row[0]
            cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [idcliente])
            nomecliente = cursor.fetchone()[0]  # Recupera o nome do cliente

            pedido_compra_cliente = {
                'idcliente': idcliente,
                'nomecliente': nomecliente,
                'datahorapedidocliente': row[1],
                'preco': row[2],
                'idpedidocompracliente': pk
            }
            return render(request, 'pedido_compracliente/pedido_compracliente_detail.html', {'pedido_compra_cliente': pedido_compra_cliente})

        raise Http404("Pedido de Compra do Cliente does not exist")

def pedido_compracliente_create(request):
    form = PedidoDetalhesForm()

    if request.method == 'POST':
        form = PedidoDetalhesForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                # Criar o pedido de compra
                data = form.cleaned_data
                cliente_id = data['idcliente'].idcliente
                datahora_formatada = data['datahorapedidocliente'].strftime("%Y-%m-%d %H:%M:%S")

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_pedido_compracliente_create(%s, %s, %s)", [
                        cliente_id, datahora_formatada, data['preco']
                    ])

                # Obter o ID do pedido recém-criado
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('pedido_compra_cliente_idpedidocompracliente_seq')")
                    id_pedido = cursor.fetchone()[0]

                # Criar detalhes para o pedido
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_pedidocompracliente_create(%s, %s, %s)", [
                        id_pedido, data['idequipamento'], data['quantidade']
                    ])

                return redirect('pedido_compracliente_list')

    return render(request, 'pedido_compracliente/pedido_compracliente_form.html', {'form': form})

 
def pedido_compracliente_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_pedido_compracliente_read(%s, %s, %s, %s, %s)", [pk, 0, None, 0, None])
            row = cursor.fetchone()

            if row:
                idcliente = row[0]
                cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [idcliente])
                nomecliente = cursor.fetchone()[0]  # Recupera o nome do cliente

                pedido_compra_cliente_data = {
                        'idcliente': idcliente,
                        'nomecliente': nomecliente,
                        'datahorapedidocliente': row[1],
                        'preco': row[2],
                        'idpedidocompracliente': pk
                }
                form = PedidoCompraclienteForm(initial=pedido_compra_cliente_data)

                if request.method == 'POST':
                    form = PedidoCompraclienteForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        with connection.cursor() as cursor:
                            cliente_id = data['idcliente'].idcliente  # Assumindo que 'id' é o campo de ID do modelo Cliente
                            datahora_formatada = data['datahorapedidocliente'].strftime("%Y-%m-%d %H:%M:%S")
                            cursor.execute("CALL sp_pedido_compracliente_update(%s, %s, %s, %s)", [pk, cliente_id, datahora_formatada, data['preco']])
                        return redirect('pedido_compracliente_list')
                    else:
                        return render(request, 'pedido_compracliente/pedido_compracliente_form.html', {'form': form, 'action': 'Atualizar'})
                else:
                    return render(request, 'pedido_compracliente/pedido_compracliente_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Pedido de Compra do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

def pedido_compracliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_pedido_compracliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])
            row = cursor.fetchone()

            if row: 
                pedido_compra_cliente = get_object_or_404(PedidoCompracliente, pk=pk)
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_pedido_compracliente_delete(%s)", [pk])
                    return redirect('pedido_compracliente_list')
                else:
                    return render(request, 'pedido_compracliente/pedido_compracliente_confirm_delete.html', {'pedido_compra_cliente': pedido_compra_cliente})
            else:
                raise Http404("Pedido de Compra do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

#detalhes pedido de compra de cliente views

def detalhes_pedidocompracliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_detalhes_pedidocompracliente()')
        columns = [col[0] for col in cursor.description]
        detalhes_pedidocompracliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_compracliente/detalhes_pedidocompracliente_list.html', {'detalhes_pedidocompracliente': detalhes_pedidocompracliente})

def detalhes_pedidocompracliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_detalhes_pedidocompracliente_read(%s, %s, %s, %s)", [pk, 0, 0, 0])  
        row = cursor.fetchone()

        if row:
            detalhes_pedido_compra_cliente = {
                'idpedidocompracliente': row[0],
                'idequipamento': row[1],
                'quantidade': row[2],
                'iddetalhespedidocompracliente': pk
            }

            print("Detalhes Pedido Compra Cliente:", detalhes_pedido_compra_cliente)

            return render(request, 'pedido_compracliente/detalhes_pedidocompracliente_detail.html', {'detalhes_pedido_compra_cliente': detalhes_pedido_compra_cliente})

        raise Http404("Detalhes do Pedido de Compra do Cliente does not exist")

def detalhes_pedidocompracliente_create(request):
    form = DetalhesPedidocompraclienteForm()

    if request.method == 'POST':
        form = DetalhesPedidocompraclienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            equipamento_id = data['idequipamento'].idequipamento  # Obtendo o ID do equipamento

            with connection.cursor() as cursor:
                cursor.execute("CALL sp_detalhes_pedidocompracliente_create(%s, %s, %s)", [
                               request.GET.get('id_pedidocompra'), equipamento_id, data['quantidade']])
            return redirect('detalhes_pedidocompracliente_list')

    return render(request, 'pedido_compracliente/detalhes_pedidocompracliente_form.html', {'form': form})

def detalhes_pedidocompracliente_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_detalhes_pedidocompracliente_read(%s)", [pk])
            row = cursor.fetchone()

            if row:
                detalhes_pedidocompracliente_data = {
                    'idpedidocompracliente': row[1],
                    'idequipamento': row[2],
                    'quantidade': row[3],
                }
                form = DetalhesPedidocompraclienteForm(initial=detalhes_pedidocompracliente_data)

                if request.method == 'POST':
                    form = DetalhesPedidocompraclienteForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_detalhes_pedidocompracliente_update(%s, %s, %s, %s)", [pk, data['idpedidocompracliente'], data['idequipamento'], data['quantidade']])
                        return redirect('detalhes_pedidocompracliente_list')
                else:
                    return render(request, 'detalhes_pedidocompracliente/detalhes_pedidocompracliente_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Detalhes do Pedido de Compra do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

def detalhes_pedidocompracliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_detalhes_pedidocompracliente_read(%s)", [pk])
            row = cursor.fetchone()  

            if row:
                detalhes_pedidocompracliente = get_object_or_404(DetalhesPedidocompracliente, pk=pk)
                if request.method == 'POST': 
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_detalhes_pedidocompracliente_delete(%s)", [pk])
                    return redirect('detalhes_pedidocompracliente_list')
                else:
                    return render(request, 'detalhes_pedidocompracliente/detalhes_pedidocompracliente_confirm_delete.html', {'detalhes_pedidocompracliente': detalhes_pedidocompracliente})
            else:
                raise Http404("Detalhes do Pedido de Compra do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

#guia de remessa read de equipamentos

def guia_remessafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_guia_remessafornecedor()')
        columns = [col[0] for col in cursor.description]
        guia_remessafornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(guia_remessafornecedor)
    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_list.html', {'guia_remessa_fornecedor': guia_remessafornecedor})
  


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