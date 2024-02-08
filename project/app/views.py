from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor, PedidoCompracliente, FolhaDeObra, DetalhesPedidocompracliente, Armazem, Faturacliente, GuiaRemessacliente, Faturafornecedor, TrabalhadorOperario, MaoDeObra
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm, PedidoDetalhesForm, PedidoCompraClienteForm, DetalhesPedidocomprafornecedorForm, GuiaRemessafornecedorForm, DetalhesGuiaremessafornecedorForm, ArmazemForm, GuiaRemessaclienteForm, DetalhesGuiaremessaclienteForm, FaturaclienteForm, FaturaclienteUpdateForm, FaturafornecedorForm, FaturafornecedorUpdateForm, Folha_de_obraForm, Detalhes_ficha_de_obraForm, TrabalhadorOperarioForm, MaoDeObraForm
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.db import connection
import json
from django.shortcuts import render, redirect
from django.http import Http404
from django.db import connection, transaction
from .forms import PedidoCompraClienteForm, PedidoDetalhesForm
from django.forms import formset_factory
import logging

def index(request):
    return render(request, 'index.html')
 

# Fornecedor views:

@permission_required('app.view_fornecedor')
def fornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_fornecedor()')
        columns = [col[0] for col in cursor.description]
        fornecedores = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        context = {
            'fornecedores': fornecedores,
            'user': request.user
        }

    return render(request, 'fornecedor/fornecedor_list.html', context)

@permission_required('app.view_fornecedor')
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
            context = {
                'fornecedor': fornecedor,
                'user': request.user
            }
            return render(request, 'fornecedor/fornecedor_detail.html', context)

        raise Http404("Fornecedor does not exist")

@permission_required('app.add_fornecedor')
def fornecedor_create(request):
    form = FornecedorForm()

    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_fornecedor_create(%s, %s, %s, %s)", [data['nomefornecedor'], data['email'], data['numerotelefonefornecedor'], data['codigopostal']])
            return redirect('fornecedor_list')

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'fornecedor/fornecedor_form.html', context)

@permission_required('app.change_fornecedor')
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
                    context = {
                        'form': form,
                        'action': 'Atualizar',
                        'user': request.user
                    }
                    return render(request, 'fornecedor/fornecedor_form.html', context)
            else:
                raise Http404("Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_fornecedor')
def fornecedor_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_fornecedor_read(%s, %s, %s, %s, %s)", [pk, '', '', '', ''])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_fornecedor_delete(%s)", [pk])
                    return redirect('fornecedor_list')
                else:
                    return render(request, 'fornecedor/fornecedor_confirm_delete.html', {'fornecedor': pk, 'user': request.user})
            else:
                raise Http404("Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")


# Cliente views

@permission_required('app.view_cliente')
def cliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_cliente()')
        columns = [col[0] for col in cursor.description]
        clientes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'cliente/cliente_list.html', {'clientes': clientes, 'user': request.user})

@permission_required('app.view_cliente')
def cliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_cliente_read(%s, %s, %s, %s, %s, %s)",
                       [pk, '', '', '', 0 , ''])  
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
            return render(request, 'cliente/cliente_detail.html', {'cliente': cliente, 'user': request.user})
        else:
            raise Http404("Cliente does not exist")
        
@permission_required('app.add_cliente')
def cliente_create(request):
    form = ClienteForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_cliente_create(%s, %s, %s, %s, %s)", [data['nomecliente'], data['numerotelefonecliente'], data['email'], data['nif'], data['codigopostal']])
            return redirect('cliente_list')

    return render(request, 'cliente/cliente_form.html', {'form': form, 'user': request.user})

@permission_required('app.change_cliente')
def cliente_update(request, pk):

    try:
        
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
                
                form = ClienteForm(initial=cliente_data)

                if request.method == 'POST':
                    
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
                    return render(request, 'cliente/cliente_form.html', {'form': form, 'action': 'Atualizar', 'user': request.user})
            else:
                raise Http404("Cliente does not exist")

    except Exception as e:
        # Lide com exceções conforme necessário
        print(e)  # Apenas para depuração, você pode usar um logger aqui
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_cliente')
def cliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            # Verifica se o cliente existe
            cursor.execute("CALL sp_cliente_read(%s, %s, %s, %s, %s, %s)", [pk, '', '', '', 0, ''])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    # Executa o procedimento armazenado para deletar o cliente
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_cliente_delete(%s)", [pk])
                    
                    return redirect('cliente_list')
                else:
                    # Se for uma requisição GET, renderiza a confirmação de exclusão
                    return render(request, 'cliente/cliente_confirm_delete.html', {'cliente': pk, 'user': request.user})
            else:
                raise Http404("Cliente does not exist")

    except Exception as e:
        print(e)  # Log do erro para depuração
        raise Http404("Erro ao processar a solicitação")


# Equipamento views

@permission_required('app.view_equipamento')
def equipamento_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_equipamento()')
        columns = [col[0] for col in cursor.description]
        equipamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'equipamento/equipamento_list.html', {'equipamentos': equipamentos, 'user': request.user })

@permission_required('app.view_equipamento')
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
            return render(request, 'equipamento/equipamento_detail.html', {'equipamento': equipamento, 'user': request.user})

        raise Http404("Equipamento does not exist")

@permission_required('app.add_equipamento')
def equipamento_create(request):
    form = EquipamentoForm()

    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_equipamento_create(%s, %s)", [data['nomeequipamento'], data['descricao']])
            return redirect('equipamento_list')

    return render(request, 'equipamento/equipamento_form.html', {'form': form, 'user': request.user})

@permission_required('app.change_equipamento')
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
                    return render(request, 'equipamento/equipamento_form.html', {'form': form, 'action': 'Atualizar', 'user': request.user})
            else:
                raise Http404("Equipamento does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_equipamento')
def equipamento_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_equipamento_read(%s, %s, %s)", [pk, '', ''])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_equipamento_delete(%s)", [pk])
                    return redirect('equipamento_list')
                else:
                    return render(request, 'equipamento/equipamento_confirm_delete.html', {'equipamento': pk, 'user': request.user})
            else:
                raise Http404("Equipamento does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

#Componente view

@permission_required('app.view_componente')
def componente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_componente()')
        columns = [col[0] for col in cursor.description]
        componentes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'componente/componente_list.html', {'componentes': componentes, 'user': request.user})

@permission_required('app.view_componente')
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
            return render(request, 'componente/componente_detail.html', {'componente': componente, 'user': request.user})

        raise Http404("Componente does not exist")

@permission_required('app.add_componente')
def componente_create(request):
    form = ComponenteForm()

    if request.method == 'POST':
        form = ComponenteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_componente_create(%s)", [data['nomecomponente']])
            return redirect('componente_list')

    return render(request, 'componente/componente_form.html', {'form': form, 'user': request.user})

@permission_required('app.change_componente')
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
                    return render(request, 'componente/componente_form.html', {'form': form, 'action': 'Atualizar', 'user': request.user})
            else:
                raise Http404("Componente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_componente')
def componente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_componente_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_componente_delete(%s)", [pk])
                    return redirect('componente_list')
                else:
                    return render(request, 'componente/componente_confirm_delete.html', {'componente': pk, 'user': request.user})
            else:
                raise Http404("Componente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")



#Pedido compra a cliente view
@permission_required('app.view_pedidocompracliente')
def pedido_compracliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_pedido_compracliente()')
        columns = [col[0] for col in cursor.description]
        pedidos_compra_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_compracliente/pedido_compracliente_list.html', {'pedidos_compra_cliente': pedidos_compra_cliente, 'user': request.user})

@permission_required('app.view_pedidocompracliente')
def pedido_compracliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_pedido_compracliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])  
        row = cursor.fetchone()

        if row:
            idcliente = row[0]
            cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [idcliente])
            nomecliente = cursor.fetchone()[0]  # Recupera o nome do cliente

            # Recuperar detalhes do pedido de compra do cliente
            cursor.execute("SELECT d.idequipamento, d.quantidade, e.nomeequipamento FROM detalhes_pedidocompracliente d INNER JOIN equipamento e ON d.idequipamento = e.idequipamento WHERE d.idpedidocompracliente = %s", [pk])
            detalhes_pedido_compra_cliente = cursor.fetchall()

            pedido_compra_cliente = {
                'idcliente': idcliente,
                'nomecliente': nomecliente,
                'datahorapedidocliente': row[1],
                'preco': row[2],
                'idpedidocompracliente': pk,
                'detalhes_pedidocompra_cliente': detalhes_pedido_compra_cliente
            }

            return render(request, 'pedido_compracliente/pedido_compracliente_detail.html', {'pedido_compra_cliente': pedido_compra_cliente, 'user': request.user})

        raise Http404("Pedido de Compra do Cliente does not exist")

@permission_required('app.add_pedidocompracliente')
def pedido_compracliente_create(request):
    form_pedido = PedidoCompraClienteForm()
    form_detalhes = PedidoDetalhesForm()

    if request.method == 'POST':
        form_pedido = PedidoCompraClienteForm(request.POST)
        form_detalhes = PedidoDetalhesForm(request.POST)

        if form_pedido.is_valid() and form_detalhes.is_valid():
            with transaction.atomic():
                # Criar o pedido de compra
                data_pedido = form_pedido.cleaned_data
                cliente_id = data_pedido['idcliente']

                with connection.cursor() as cursor:
                    cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [cliente_id])
                    nome_cliente = cursor.fetchone()[0]

                    cursor.execute("CALL sp_pedido_compracliente_create(%s, %s, %s)", [
                        cliente_id, None, data_pedido['preco']
                    ])

                # Obter o ID do pedido recém-criado
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('pedido_compra_cliente_idpedidocompracliente_seq')")
                    id_pedido = cursor.fetchone()[0]

                # Criar detalhes para o pedido (suportando múltiplos detalhes)
                idequipamentos = request.POST.getlist('idequipamento')
                quantidades = request.POST.getlist('quantidade')

                for idequipamento, quantidade in zip(idequipamentos, quantidades):
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_detalhes_pedidocompracliente_create(%s, %s, %s)", [
                            id_pedido, idequipamento, quantidade
                        ])

            # Adicione nome_cliente ao contexto do template
            context = {
                'form_pedido': form_pedido,
                'form_detalhes': form_detalhes,
                'nome_cliente': nome_cliente,
            }

            return render(request, 'pedido_compracliente/pedido_compracliente_list.html', context)

    return render(request, 'pedido_compracliente/pedido_compracliente_form.html', {'form_pedido': form_pedido, 'form_detalhes': form_detalhes, 'user': request.user})

@permission_required('app.delete_pedidocompracliente')
def pedido_compracliente_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes do pedido de compra do cliente
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_pedidocompracliente_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar o pedido de compra do cliente
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_pedido_compracliente_delete(%s)", [pk])

                return redirect('pedido_compracliente_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'pedido_compracliente/pedido_compracliente_confirm_delete.html', {'idpedidocompracliente': pk, 'user': request.user})

#Pedido compra a fornecedor view

@permission_required('app.view_pedidocomprafornecedor')
def pedido_comprafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_pedido_comprafornecedor()')
        columns = [col[0] for col in cursor.description]
        pedidos_compra_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_list.html', {'pedidos_compra_fornecedor': pedidos_compra_fornecedor, 'user': request.user})

@permission_required('app.view_pedidocomprafornecedor')
def pedido_comprafornecedor_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_pedido_comprafornecedor_read(%s, %s, %s, %s)", [pk, 0, None, 0])  
        row = cursor.fetchone()

        if row:
            idfornecedor = row[0]
            cursor.execute("SELECT nomefornecedor FROM fornecedor WHERE idfornecedor = %s", [idfornecedor])
            nomefornecedor = cursor.fetchone()[0]  # Recupera o nome do fornecedor

            # Recuperar detalhes do pedido de compra do fornecedor
            cursor.execute("SELECT d.idcomponente, d.quantidade, c.nomecomponente FROM detalhes_pedidocomprafornecedor d INNER JOIN componente c ON d.idcomponente = c.idcomponente WHERE d.idpedidocomprafornecedor = %s", [pk])
            detalhes_pedido_compra_fornecedor = cursor.fetchall()
            print(detalhes_pedido_compra_fornecedor)

            pedido_compra_fornecedor = {
                'idfornecedor': idfornecedor,
                'nomefornecedor': nomefornecedor,
                'datahorapedidofornecedor': row[1],
                'preco': row[2],
                'idpedidocomprafornecedor': pk,
                'detalhes_pedidocompra_fornecedor': detalhes_pedido_compra_fornecedor
            }

            return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_detail.html', {'pedido_compra_fornecedor': pedido_compra_fornecedor, 'user': request.user})

        raise Http404("Pedido de Compra do Fornecedor does not exist")

@permission_required('app.add_pedidocomprafornecedor')
def pedido_comprafornecedor_create(request):
    form_pedido = PedidoCompraFornecedorForm()
    form_detalhes = DetalhesPedidocomprafornecedorForm()

    if request.method == 'POST':
        form_pedido = PedidoCompraFornecedorForm(request.POST)
        form_detalhes = DetalhesPedidocomprafornecedorForm(request.POST)

        if form_pedido.is_valid() and form_detalhes.is_valid():
            with transaction.atomic():
                # Criar o pedido de compra para fornecedor
                data_pedido = form_pedido.cleaned_data
                fornecedor_id = data_pedido['idfornecedor']

                with connection.cursor() as cursor:
                    cursor.execute("SELECT nomefornecedor FROM fornecedor WHERE idfornecedor = %s", [fornecedor_id])
                    nome_fornecedor = cursor.fetchone()[0]

                    cursor.execute("CALL sp_pedido_comprafornecedor_create(%s, %s, %s)", [
                        fornecedor_id, None, data_pedido['preco']
                    ])

                # Obter o ID do pedido recém-criado
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('pedido_compra_idpedidocompra_seq')")
                    id_pedido = cursor.fetchone()[0]

                # Criar detalhes para o pedido (suportando múltiplos detalhes)
                idcomponentes = request.POST.getlist('idcomponente')
                quantidades = request.POST.getlist('quantidade')

                for idcomponente, quantidade in zip(idcomponentes, quantidades):
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_detalhes_pedidocomprafornecedor_create(%s, %s, %s)", [
                            id_pedido, idcomponente, quantidade
                        ])

            # Adicione nome_fornecedor ao contexto do template
            context = {
                'form_pedido': form_pedido,
                'form_detalhes': form_detalhes,
                'nome_fornecedor': nome_fornecedor,
            }

            return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_list.html', context)

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_form.html', {'form_pedido': form_pedido, 'form_detalhes': form_detalhes, 'user': request.user})

@permission_required('app.delete_pedidocomprafornecedor')
def pedido_comprafornecedor_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes do pedido de compra para fornecedor
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_pedidocomprafornecedor_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar o pedido de compra para fornecedor
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_pedido_comprafornecedor_delete(%s)", [pk])

                return redirect('pedido_comprafornecedor_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_confirm_delete.html', {'idpedidocomprafornecedor': pk, 'user': request.user})

# views da guia de remessa do fornecedor

@permission_required('app.view_guiaremessafornecedor')
def guia_remessafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_guia_remessafornecedor()')
        columns = [col[0] for col in cursor.description]
        guias_remessa_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_list.html', {'guias_remessa_fornecedor': guias_remessa_fornecedor, 'user': request.user})

@permission_required('app.view_guiaremessafornecedor')
def guia_remessafornecedor_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_guia_remessafornecedor_read(%s, %s, %s)", [pk, 0, None])  
        row = cursor.fetchone()

        if row:
            idfornecedor = row[0]
            cursor.execute("SELECT nomefornecedor FROM fornecedor WHERE idfornecedor = %s", [idfornecedor])
            nomefornecedor = cursor.fetchone()  # Recupera o nome do fornecedor

            # Recuperar detalhes da guia de remessa para fornecedor, incluindo informações do armazém
            cursor.execute("SELECT d.idcomponente, d.quantidade, c.nomecomponente, a.codigopostal FROM detalhes_guiaremessafornecedor d INNER JOIN componente c ON d.idcomponente = c.idcomponente INNER JOIN armazem a ON d.idarmazem = a.idarmazem WHERE d.idguiaremessafornecedor = %s", [pk])
            detalhes_guia_remessa_fornecedor = cursor.fetchall()

            cursor.execute("SELECT idpedidocomprafornecedor FROM guia_remessafornecedor WHERE idguiaremessafornecedor = %s", [pk])
            idpedidocomprafornecedor = cursor.fetchone()[0]

            print("Detalhes da Guia:", detalhes_guia_remessa_fornecedor)

            guia_remessa_fornecedor = {
                'idfornecedor': idfornecedor,
                'nomefornecedor': nomefornecedor,
                'datahoraguiafornecedor': row[1],
                'idguiaremessafornecedor': pk,
                'idpedidocomprafornecedor': idpedidocomprafornecedor,
                'detalhes_guiaremessafornecedor': detalhes_guia_remessa_fornecedor
            }
            

            return render(request, 'guia_remessafornecedor/guia_remessafornecedor_detail.html', {'guia_remessa_fornecedor': guia_remessa_fornecedor, 'user': request.user})

        raise Http404("Guia de Remessa para Fornecedor does not exist")

@permission_required('app.add_guiaremessafornecedor')
def guia_remessafornecedor_create(request):
    form_guia_remessa = GuiaRemessafornecedorForm()
    form_detalhes = DetalhesGuiaremessafornecedorForm()

    if request.method == 'POST':
        form_guia_remessa = GuiaRemessafornecedorForm(request.POST)
        form_detalhes = DetalhesGuiaremessafornecedorForm(request.POST)

        if form_guia_remessa.is_valid() and form_detalhes.is_valid():
            with transaction.atomic():
                # Criar a guia de remessa para fornecedor
                data_guia_remessa = form_guia_remessa.cleaned_data
                pedido_compra_fornecedor_id = data_guia_remessa['idpedidocomprafornecedor']

                with connection.cursor() as cursor:
                    cursor.execute("SELECT nomefornecedor FROM fornecedor WHERE idfornecedor = (SELECT idfornecedor FROM pedido_comprafornecedor WHERE idpedidocomprafornecedor = %s)", [pedido_compra_fornecedor_id])
                    nome_fornecedor = cursor.fetchone()[0]

                    cursor.execute("CALL sp_guia_remessafornecedor_create(%s, %s)", [
                        pedido_compra_fornecedor_id, data_guia_remessa['datahoraguiafornecedor']
                    ])

                # Obter o ID da guia de remessa recém-criada
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('guia_remessa_idguiaremessa_seq')")
                    id_guia_remessa = cursor.fetchone()[0]

                # Criar detalhes para a guia de remessa (suportando múltiplos detalhes)
                idarmazens = request.POST.getlist('idarmazem')
                idcomponentes = request.POST.getlist('idcomponente')
                quantidades = request.POST.getlist('quantidade')

                for idarmazem, idcomponente, quantidade in zip(idarmazens, idcomponentes, quantidades):
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_detalhes_guiaremessafornecedor_create(%s, %s, %s, %s, %s)", [
                           idarmazem, id_guia_remessa, idcomponente, quantidade, None
                        ])

            # Adicione nome_fornecedor ao contexto do template
            context = {
                'form_guia_remessa': form_guia_remessa,
                'form_detalhes': form_detalhes,
                'nome_fornecedor': nome_fornecedor,
            }

            return render(request, 'guia_remessafornecedor/guia_remessafornecedor_list.html', context)

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_form.html', {'form_guia_remessa': form_guia_remessa, 'form_detalhes': form_detalhes, 'user': request.user})

@permission_required('app.delete_guiaremessafornecedor')
def guia_remessafornecedor_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes da guia de remessa para fornecedor
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_guiaremessafornecedor_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar a guia de remessa para fornecedor
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_guia_remessafornecedor_delete(%s)", [pk])

                return redirect('guia_remessafornecedor_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_confirm_delete.html', {'idguiaremessafornecedor': pk, 'user': request.user})

# views do armazem

@permission_required('app.view_armazem')
def armazem_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_armazem()')
        columns = [col[0] for col in cursor.description]
        armazens = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'armazem/armazem_list.html', {'armazens': armazens, 'user': request.user})

@permission_required('app.view_armazem')
def armazem_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_armazem_read(%s, %s)", [pk, ''])
        row = cursor.fetchone()

        if row:
            armazem = {
                'codigopostal': row[0],
                'idarmazem': pk
            }
            return render(request, 'armazem/armazem_detail.html', {'armazem': armazem, 'user': request.user})

        raise Http404("Armazem does not exist")

@permission_required('app.add_armazem')
def armazem_create(request):
    form = ArmazemForm()

    if request.method == 'POST':
        form = ArmazemForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_armazem_create(%s)", [data['codigopostal']])
            return redirect('armazem_list')

    return render(request, 'armazem/armazem_form.html', {'form': form, 'user': request.user})

@permission_required('app.change_armazem')
def armazem_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_armazem_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                armazem_data = {
                    'codigopostal': row[0],
                }
                form = ArmazemForm(initial=armazem_data)

                if request.method == 'POST':
                    form = ArmazemForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_armazem_update(%s, %s)", [pk, data['codigopostal']])
                        return redirect('armazem_list')
                else:
                    return render(request, 'armazem/armazem_form.html', {'form': form, 'action': 'Atualizar', 'user': request.user})
            else:
                raise Http404("Armazém does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_armazem')
def armazem_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_armazem_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_armazem_delete(%s)", [pk])
                    return redirect('armazem_list')
                else:
                    return render(request, 'armazem/armazem_confirm_delete.html', {'armazem': pk, 'user': request.user})
            else:
                raise Http404("Armazém does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#views da guia de remessa ao cliente

@permission_required('app.view_guiaremessacliente')
def guia_remessacliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_guia_remessacliente()')
        columns = [col[0] for col in cursor.description]
        guias_remessa_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'guia_remessacliente/guia_remessacliente_list.html', {'guias_remessa_cliente': guias_remessa_cliente, 'user': request.user})

@permission_required('app.view_guiaremessacliente')
def guia_remessacliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_guia_remessacliente_read(%s, %s, %s)", [pk, 0, None])  
        row = cursor.fetchone()

        if row:
            idcliente = row[0]
            cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [idcliente])
            nomecliente = cursor.fetchone()  # Recupera o nome do cliente

            # Recuperar detalhes da guia de remessa para cliente, incluindo informações do armazém
            cursor.execute("SELECT d.idequipamento, d.quantidade, c.nomeequipamento FROM detalhes_guiaremessacliente d INNER JOIN equipamento c ON d.idequipamento = c.idequipamento INNER JOIN armazem a ON d.idarmazem = a.idarmazem WHERE d.idguiaremessacliente = %s", [pk])
            detalhes_guia_remessa_cliente = cursor.fetchall()

            cursor.execute("SELECT idpedidocompracliente FROM guia_remessacliente WHERE idguiaremessacliente = %s", [pk])
            idpedidocompracliente = cursor.fetchone()[0]

            print("Detalhes da Guia:", detalhes_guia_remessa_cliente)

            guia_remessa_cliente = {
                'idcliente': idcliente,
                'nomecliente': nomecliente,
                'datahoraguiacliente': row[1],
                'idguiaremessacliente': pk,
                'idpedidocompracliente': idpedidocompracliente,
                'detalhes_guiaremessacliente': detalhes_guia_remessa_cliente
            }

            return render(request, 'guia_remessacliente/guia_remessacliente_detail.html', {'guia_remessa_cliente': guia_remessa_cliente, 'user': request.user})

        raise Http404("Guia de Remessa para Cliente does not exist")

@permission_required('app.add_guiaremessacliente')
def guia_remessacliente_create(request):
    form_guia_remessa = GuiaRemessaclienteForm()
    form_detalhes = DetalhesGuiaremessaclienteForm()

    if request.method == 'POST':
        print(request.POST)
        form_guia_remessa = GuiaRemessaclienteForm(request.POST)
        form_detalhes = DetalhesGuiaremessaclienteForm(request.POST)

        if form_guia_remessa.is_valid() and form_detalhes.is_valid():
            with transaction.atomic():
                # Criar a guia de remessa para cliente
                data_guia_remessa = form_guia_remessa.cleaned_data
                pedido_compra_cliente_id = data_guia_remessa['idpedidocompracliente']

                with connection.cursor() as cursor:
                    cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = (SELECT idcliente FROM pedido_compracliente WHERE idpedidocompracliente = %s)", [pedido_compra_cliente_id])
                    nome_cliente = cursor.fetchone()[0]

                    cursor.execute("CALL sp_guia_remessacliente_create(%s, %s)", [
                        pedido_compra_cliente_id, data_guia_remessa['datahoraguiacliente']
                    ])

                # Obter o ID da guia de remessa recém-criada
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('guia_remessacliente_idguiaremessacliente_seq')")
                    id_guia_remessa = cursor.fetchone()[0]

                # Criar detalhes para a guia de remessa (suportando múltiplos detalhes)
                idarmazens = request.POST.getlist('idarmazem')
                idequipamentos = request.POST.getlist('idequipamento')
                quantidades = request.POST.getlist('quantidade')

                for idarmazem, idequipamento, quantidade in zip(idarmazens, idequipamentos, quantidades):
                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_detalhes_guiaremessacliente_create(%s, %s, %s, %s, %s)", [
                            idarmazem, id_guia_remessa, quantidade, idequipamento, None
                        ])

            # Adicione nome_cliente ao contexto do template
            context = {
                'form_guia_remessa': form_guia_remessa,
                'form_detalhes': form_detalhes,
                'nome_cliente': nome_cliente,
            }

            return render(request, 'guia_remessacliente/guia_remessacliente_list.html', context)

    return render(request, 'guia_remessacliente/guia_remessacliente_form.html', {'form_guia_remessa': form_guia_remessa, 'form_detalhes': form_detalhes, 'user': request.user})

@permission_required('app.delete_guiaremessacliente')
def guia_remessacliente_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes da guia de remessa para cliente
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_guiaremessacliente_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar a guia de remessa para cliente
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_guia_remessacliente_delete(%s)", [pk])

                return redirect('guia_remessacliente_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'guia_remessacliente/guia_remessacliente_confirm_delete.html', {'idguiaremessacliente': pk, 'user': request.user})

#views das  faturas dos clientes

@permission_required('app.view_faturacliente')
def faturacliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_faturacliente()')
        columns = [col[0] for col in cursor.description]
        faturas_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(faturas_cliente)  # Adicione este print para verificar os dados na console do servidor

    return render(request, 'faturacliente/faturacliente_list.html', {'faturaclientes': faturas_cliente})

@permission_required('app.view_faturacliente')
def faturacliente_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_faturacliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])  # Ajuste conforme necessário
        row = cursor.fetchone()

        if row:
            fatura_cliente = {
                'idguiaremessacliente': row[0],
                'datahorafaturacliente': row[1],
                'preco': row[2],
                'idfaturacliente': pk
                # Adicione outros campos conforme necessário
            }

            return render(request, 'faturacliente/faturacliente_detail.html',{'faturacliente': fatura_cliente})

        raise Http404("Fatura do Cliente does not exist")

@permission_required('app.add_faturacliente')
def faturacliente_create(request):
    form_fatura = FaturaclienteForm()

    if request.method == 'POST':
        form_fatura = FaturaclienteForm(request.POST)

        if form_fatura.is_valid():
            with transaction.atomic():
                # Criar a fatura para cliente
                data_fatura = form_fatura.cleaned_data
                idguiaremessacliente = data_fatura['idguiaremessacliente']

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_faturacliente_create(%s, %s, %s)", [
                        idguiaremessacliente, data_fatura['datahorafaturacliente'], data_fatura['preco']
                    ])

            return redirect('faturacliente_list')  # Redirecionar para a lista de faturas

    return render(request, 'faturacliente/faturacliente_form.html', {'form_fatura': form_fatura})


@permission_required('app.change_faturacliente')
def faturacliente_update(request, pk):
    if request.method == 'POST':
        form_fatura = FaturaclienteUpdateForm(request.POST)

        if form_fatura.is_valid():
            with transaction.atomic():
                # Atualizar a fatura do cliente
                data_fatura = form_fatura.cleaned_data
                idguiaremessacliente = data_fatura.get('idguiaremessacliente', None)

                with connection.cursor() as cursor:
                    # Verifica se a fatura existe
                    cursor.execute("SELECT * FROM faturacliente WHERE idfaturacliente = %s", [pk])
                    row = cursor.fetchone()

                    if row:
                        # Se a fatura existe, execute a atualização
                        cursor.execute("CALL sp_faturacliente_update(%s, %s, %s, %s)", [
                            pk, idguiaremessacliente, data_fatura['datahorafaturacliente'], data_fatura['preco']
                        ])
                        return redirect('faturacliente_list')  # Redirecionar para a lista de faturas
                    else:
                        raise Http404("Fatura does not exist")

    else:
        # Obtém os dados da fatura diretamente do banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM faturacliente WHERE idfaturacliente = %s", [pk])
            row = cursor.fetchone()

            if row:
                # Se a fatura existe, inicialize o formulário com os dados da fatura
                fatura_data = {
                    'datahorafaturacliente': row[1],
                    'preco': row[2]
                }
                form_fatura = FaturaclienteUpdateForm(initial=fatura_data)
            else:
                raise Http404("Fatura does not exist")

    return render(request, 'faturacliente/faturacliente_form_update.html', {'form_fatura': form_fatura, 'user': request.user})

@permission_required('app.delete_faturacliente')
def faturacliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_faturacliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])  # Ajuste conforme necessário
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_faturacliente_delete(%s)", [pk])
                    return redirect('faturacliente_list')
                else:
                    return render(request, 'faturacliente/faturacliente_confirm_delete.html', {'pk': pk, 'user': request.user})
            else:
                raise Http404("Fatura do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#views fatura fornecedor

@permission_required('app.view_faturafornecedor')
def faturafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_faturafornecedor()')
        columns = [col[0] for col in cursor.description]
        faturas_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(faturas_fornecedor)  # Adicione esta linha para imprimir os dados no console
    
    return render(request, 'faturafornecedor/faturafornecedor_list.html', {'faturafornecedores': faturas_fornecedor, 'user': request.user})

@permission_required('app.view_faturafornecedor')
def faturafornecedor_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_faturafornecedor_read(%s, %s, %s, %s)", [pk, 0, None, 0])  # Ajuste conforme necessário
        row = cursor.fetchone()

        if row:
            fatura_fornecedor = {
                'idguiaremessafornecedor': row[0],
                'datahorafaturafornecedor': row[1],
                'preco': row[2],
                'idfaturafornecedor': pk
                # Adicione outros campos conforme necessário
            }
            print(f"ID da Guia de Remessa do Fornecedor: {Faturafornecedor.idguiaremessafornecedor}")

            return render(request, 'faturafornecedor/faturafornecedor_detail.html', {'faturafornecedor': fatura_fornecedor, 'user': request.user})

        raise Http404("Fatura do Fornecedor does not exist")

@permission_required('app.add_faturafornecedor')
def faturafornecedor_create(request):
    form_fatura = FaturafornecedorForm()

    if request.method == 'POST':
        form_fatura = FaturafornecedorForm(request.POST)

        if form_fatura.is_valid():
            print("Formulário válido. Tentando criar a fatura.")
            with transaction.atomic():
                # Criar a fatura para fornecedor
                data_fatura = form_fatura.cleaned_data
                idguiaremessafornecedor = data_fatura['idguiaremessafornecedor']

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_faturafornecedor_create(%s, %s, %s)", [
                        idguiaremessafornecedor, data_fatura['datahorafaturafornecedor'], data_fatura['preco']
                    ])

            print("Fatura criada com sucesso. Redirecionando para faturafornecedor_list.")
            return redirect('faturafornecedor_list')  # Redirecionar para a lista de faturas de fornecedor

    return render(request, 'faturafornecedor/faturafornecedor_form.html', {'form_fatura': form_fatura, 'user': request.user})

@permission_required('app.change_faturafornecedor')
def faturafornecedor_update(request, pk):
    if request.method == 'POST':
        form_fatura = FaturafornecedorUpdateForm(request.POST)

        if form_fatura.is_valid():
            with transaction.atomic():
                # Atualizar a fatura do fornecedor
                data_fatura = form_fatura.cleaned_data
                idguiaremessafornecedor = data_fatura.get('idguiaremessafornecedor', None)

                with connection.cursor() as cursor:
                    # Verifica se a fatura existe
                    cursor.execute("SELECT * FROM faturafornecedor WHERE idfaturafornecedor = %s", [pk])
                    row = cursor.fetchone()

                    if row:
                        # Se a fatura existe, execute a atualização
                        cursor.execute("CALL sp_faturafornecedor_update(%s, %s, %s, %s)", [
                            pk, idguiaremessafornecedor, data_fatura['datahorafaturafornecedor'], data_fatura['preco']
                        ])
                        return redirect('faturafornecedor_list')  # Redirecionar para a lista de faturas de fornecedor
                    else:
                        raise Http404("Fatura does not exist")

    else:
        # Obtém os dados da fatura diretamente do banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM faturafornecedor WHERE idfaturafornecedor = %s", [pk])
            row = cursor.fetchone()

            if row:
                # Se a fatura existe, inicialize o formulário com os dados da fatura
                fatura_data = {
                    'datahorafaturafornecedor': row[1],
                    'preco': row[2]
                }
                form_fatura = FaturafornecedorUpdateForm(initial=fatura_data)
            else:
                raise Http404("Fatura does not exist")

    return render(request, 'faturafornecedor/faturafornecedor_form_update.html', {'form_fatura': form_fatura, 'user': request.user})

@permission_required('app.delete_faturafornecedor')
def faturafornecedor_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            # Ajuste conforme necessário para a sua implementação
            cursor.execute("CALL sp_faturafornecedor_read(%s, %s, %s, %s)", [pk, 0, None, 0])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_faturafornecedor_delete(%s)", [pk])
                    return redirect('faturafornecedor_list')
                else:
                    return render(request, 'faturafornecedor/faturafornecedor_confirm_delete.html', {'pk': pk, 'user': request.user})
            else:
                raise Http404("Fatura do Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#folha de obra views

@permission_required('app.view_folhadeobra')
def folha_de_obra_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_folha_de_obra()')
        columns = [col[0] for col in cursor.description]
        folhas_de_obra = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        context = {
            'folhas_de_obra': folhas_de_obra,
            'user': request.user  # Passando o objeto de usuário para o contexto do template
        }

    return render(request, 'folha_de_obra/folha_de_obra_list.html', context)

@permission_required('app.view_folhadeobra')
def folha_de_obra_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_folha_de_obra_read(%s, %s, %s, %s, %s, %s, %s)", [pk, 0, 0, None, None, 0, 0])  
        row = cursor.fetchone()

        if row:
            idmaodeobra = row[0]
            idequipamento = row[1]
            idarmazem = row[4]

            cursor.execute("SELECT tipodemaodeobra FROM mao_de_obra WHERE idmaodeobra = %s", [idmaodeobra])
            tipodemaodeobra = cursor.fetchone()[0]  # Recupera o nome da mão de obra

            cursor.execute("SELECT nomeequipamento FROM equipamento WHERE idequipamento = %s", [idequipamento])
            nomeequipamento = cursor.fetchone()[0]  # Recupera o nome do equipamento

            cursor.execute("SELECT codigopostal FROM armazem WHERE idarmazem = %s", [idarmazem])
            codigopostal = cursor.fetchone()[0]  # Recupera o código postal do armazém

            # Recuperar detalhes da folha de obra, incluindo informações do armazém
            cursor.execute("SELECT idcomponente, quantidade, idarmazem, datahoradetalhesfolhadeobra FROM detalhes_folha_de_obra WHERE idfolhadeobra = %s", [pk])
            detalhes_folha_de_obra = cursor.fetchall()


            folha_de_obra = {
                'idmaodeobra': idmaodeobra,
                'nomemaodeobra': tipodemaodeobra,
                'idequipamento': idequipamento,
                'nomeequipamento': nomeequipamento,
                'datahorainicio': row[2],
                'datahorafim': row[3],
                'idarmazem': idarmazem,
                'codigopostal': codigopostal,
                'precomedio': row[5],
                'idfolhadeobra': pk,
                'detalhes_folha_de_obra': detalhes_folha_de_obra
            }
            
            print(f"Folha de Obra: {folha_de_obra}")

            return render(request, 'folha_de_obra/folha_de_obra_detail.html', {'folha_de_obra': folha_de_obra, 'user': request.user})

        raise Http404("Folha de Obra does not exist")
    
@permission_required('app.add_folhadeobra')
def folha_de_obra_create(request):
    form_folha_obra = Folha_de_obraForm()
    form_detalhes = Detalhes_ficha_de_obraForm()

    if request.method == 'POST':
        form_folha_obra = Folha_de_obraForm(request.POST)
        form_detalhes = Detalhes_ficha_de_obraForm(request.POST)

        if form_folha_obra.is_valid() and form_detalhes.is_valid():
            with transaction.atomic():
                # Criar a folha de obra
                data_folha_obra = form_folha_obra.cleaned_data

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_folha_de_obra_create(%s, %s, %s, %s, %s, %s)", [
                        data_folha_obra['idmaodeobra'], data_folha_obra['idequipamento'],
                        data_folha_obra['datahorainicio'], data_folha_obra['datahorafim'],
                        data_folha_obra['idarmazem'], data_folha_obra['precomedio']
                    ])

                # Obter o ID da folha de obra recém-criada
                with connection.cursor() as cursor:
                    cursor.execute("SELECT currval('folha_de_obra_idfolhadeobra_seq')")
                    id_folha_obra = cursor.fetchone()[0]

                # Criar detalhes para a folha de obra (suportando múltiplos detalhes)
                idcomponentes = request.POST.getlist('idcomponente')
                idarmazens = request.POST.getlist('idarmazem')
                quantidades = request.POST.getlist('quantidade')
                datahora = request.POST.getlist('datahoradetalhesfolhadeobra')

                for idcomponente, idarmazem, quantidade, datahoradetalhesfolhadeobra in zip(idcomponentes, idarmazens, quantidades, datahora):
                    # Adiciona instruções de impressão
                    print(f"idcomponente: {idcomponente}, idarmazem: {idarmazem}, quantidade: {quantidade}, data: {datahoradetalhesfolhadeobra}")


                    with connection.cursor() as cursor:
                        cursor.execute("CALL sp_detalhes_folha_de_obra_create(%s, %s, %s, %s, %s)", [
                            id_folha_obra, idcomponente, quantidade, idarmazem, datahoradetalhesfolhadeobra
                        ])

            return redirect('folha_de_obra_list')  # Redirecionar para a lista de folhas de obra

    return render(request, 'folha_de_obra/folha_de_obra_form.html', {'form_folha_obra': form_folha_obra, 'form_detalhes': form_detalhes, 'user': request.user})

@permission_required('app.delete_folhadeobra')
def folha_de_obra_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes da folha de obra
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_folha_de_obra_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar a folha de obra
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_folha_de_obra_delete(%s)", [pk])

                return redirect('folha_de_obra_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'folha_de_obra/folha_de_obra_confirm_delete.html', {'idfolhadeobra': pk, 'user': request.user})

#views trabalhador operario

@permission_required('app.view_trabalhadoroperario')
def trabalhador_operario_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_trabalhador_operario()')
        columns = [col[0] for col in cursor.description]
        trabalhadores_operarios = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'trabalhador_operario/trabalhador_operario_list.html', {'trabalhadores_operarios': trabalhadores_operarios, 'user': request.user})

@permission_required('app.view_trabalhadoroperario')
def trabalhador_operario_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_trabalhador_operario_read(%s, %s, %s)", [pk, '', ''])  # Ajuste conforme necessário
        row = cursor.fetchone()

        if row:
            trabalhador_operario = {
                'nome': row[0],
                'email': row[1],
                'idtrabalhadoroperario': pk
                # Adicione outros campos conforme necessário
            }
            return render(request, 'trabalhador_operario/trabalhador_operario_detail.html', {'trabalhador_operario': trabalhador_operario, 'user': request.user})

        raise Http404("Trabalhador Operário does not exist")

@permission_required('app.add_trabalhadoroperario')
def trabalhador_operario_create(request):
    form = TrabalhadorOperarioForm()

    if request.method == 'POST':
        form = TrabalhadorOperarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_trabalhador_operario_create(%s, %s)", [data['nome'], data['email']])
            return redirect('trabalhador_operario_list')

    return render(request, 'trabalhador_operario/trabalhador_operario_form.html', {'form': form, 'user': request.user})

@permission_required('app.change_trabalhadoroperario')
def trabalhador_operario_update(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_trabalhador_operario_read(%s, %s, %s)", [pk, '', ''])  # Ajuste conforme necessário
            row = cursor.fetchone()

            if row:
                trabalhador_operario_data = {
                    'nome': row[0],
                    'email': row[1],
                    # Adicione outros campos conforme necessário
                }
                form = TrabalhadorOperarioForm(initial=trabalhador_operario_data)

                if request.method == 'POST':
                    form = TrabalhadorOperarioForm(request.POST)
                    if form.is_valid():
                        data = form.cleaned_data
                        
                        # Execute este procedimento para verificar a passagem de valores
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_trabalhador_operario_update(%s, %s, %s)", [pk, data['nome'], data['email']])
                        return redirect('trabalhador_operario_list')
                else:
                    return render(request, 'trabalhador_operario/trabalhador_operario_form.html', {'form': form, 'action': 'Atualizar', 'user': request.user})
            else:
                raise Http404("Trabalhador Operário does not exist")
    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

@permission_required('app.delete_trabalhadoroperario')
def trabalhador_operario_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_trabalhador_operario_read(%s, %s, %s)", [pk, '', ''])  # Ajuste conforme necessário
            row = cursor.fetchone()
            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_trabalhador_operario_delete(%s)", [pk])
                    return redirect('trabalhador_operario_list')
                else:
                    return render(request, 'trabalhador_operario/trabalhador_operario_confirm_delete.html', {'trabalhador_operario': pk, 'user': request.user})
            else:
                raise Http404("Trabalhador Operário does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#views mao de obra

@permission_required('app.view_maodeobra')
def mao_de_obra_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_mao_de_obra()')
        columns = [col[0] for col in cursor.description]
        maos_de_obra = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(maos_de_obra)
    return render(request, 'mao_de_obra/mao_de_obra_list.html', {'maos_de_obra': maos_de_obra, 'user': request.user})

@permission_required('app.view_maodeobra')
def mao_de_obra_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_mao_de_obra_read(%s, %s, %s, %s)", [pk, 0, '', 0])
        row = cursor.fetchone()

        idtrabalhadoroperario = row[0]
        cursor.execute("SELECT nome FROM trabalhador_operario WHERE idtrabalhadoroperario = %s", [idtrabalhadoroperario])
        nome = cursor.fetchone()[0]  # Recupera o nome do cliente


        if row:
            mao_de_obra = {
                'idtrabalhadoroperario': row[0],
                'nome': nome,
                'tipodemaodeobra': row[1],
                'custo_hora': row[2],
                'idmaodeobra': pk
                # Adicione outros campos conforme necessário
            }

            return render(request, 'mao_de_obra/mao_de_obra_detail.html', {'mao_de_obra': mao_de_obra, 'user': request.user})

        raise Http404("Mão de Obra does not exist")

@permission_required('app.add_maodeobra')
def mao_de_obra_create(request):
    form_mao_de_obra = MaoDeObraForm()

    if request.method == 'POST':
        form_mao_de_obra = MaoDeObraForm(request.POST)

        if form_mao_de_obra.is_valid():
            with transaction.atomic():
                # Criar a mão de obra
                data_mao_de_obra = form_mao_de_obra.cleaned_data
                idtrabalhadoroperario = data_mao_de_obra['idtrabalhadoroperario'].idtrabalhadoroperario
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_mao_de_obra_create(%s, %s, %s)", [
                        idtrabalhadoroperario,  # Ajuste aqui
                        data_mao_de_obra['tipodemaodeobra'],
                        data_mao_de_obra['custo_hora']
                    ])

            return redirect('mao_de_obra_list')  # Redirecionar para a lista de mão de obra

    return render(request, 'mao_de_obra/mao_de_obra_form.html', {'form_mao_de_obra': form_mao_de_obra, 'user': request.user})

@permission_required('app.change_maodeobra')
def mao_de_obra_update(request, pk):
    if request.method == 'POST':
        form_mao_de_obra = MaoDeObraForm(request.POST)

        if form_mao_de_obra.is_valid():
            with transaction.atomic():
                # Atualizar a mão de obra
                data_mao_de_obra = form_mao_de_obra.cleaned_data
                idtrabalhadoroperario = data_mao_de_obra['idtrabalhadoroperario'].idtrabalhadoroperario
                with connection.cursor() as cursor:
                    # Verifica se a mão de obra existe
                    cursor.execute("SELECT * FROM mao_de_obra WHERE idmaodeobra = %s", [pk])
                    row = cursor.fetchone()

                    if row:
                        # Se a mão de obra existe, execute a atualização
                        cursor.execute("CALL sp_mao_de_obra_update(%s, %s, %s, %s)", [
                            pk, idtrabalhadoroperario, data_mao_de_obra['tipodemaodeobra'],
                            data_mao_de_obra['custo_hora']
                        ])
                        return redirect('mao_de_obra_list')  # Redirecionar para a lista de mão de obra
                    else:
                        raise Http404("Mão de obra does not exist")

    else:
        # Obtém os dados da mão de obra diretamente do banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM mao_de_obra WHERE idmaodeobra = %s", [pk])
            row = cursor.fetchone()

            if row:
                # Se a mão de obra existe, inicialize o formulário com os dados da mão de obra
                mao_de_obra_data = {
                    'idtrabalhadoroperario': row[1],  # Substitua pelo nome correto do campo no seu banco de dados
                    'tipodemaodeobra': row[2],
                    'custo_hora': row[3]
                }
                form_mao_de_obra = MaoDeObraForm(initial=mao_de_obra_data)
            else:
                raise Http404("Mão de obra does not exist")

    return render(request, 'mao_de_obra/mao_de_obra_form_update.html', {'form_mao_de_obra': form_mao_de_obra, 'user': request.user})


@permission_required('app.delete_maodeobra')
def mao_de_obra_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            # Ajuste conforme necessário
            cursor.execute("CALL sp_mao_de_obra_read(%s, %s, %s, %s)", [pk, 0, '', 0])
            row = cursor.fetchone()

            if row:
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_mao_de_obra_delete(%s)", [pk])
                    return redirect('mao_de_obra_list')
                else:
                    return render(request, 'mao_de_obra/mao_de_obra_confirm_delete.html', {'pk': pk, 'user': request.user})
            else:
                raise Http404("Mão de Obra does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")

#view exportar json
    
def exportar_pedidos_compra_json(_request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_pedido_compra_json(array_agg(idpedidocomprafornecedor)) FROM pedido_comprafornecedor")
        pedidos_compra_json = cursor.fetchone()[0]
    
    response = HttpResponse(pedidos_compra_json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="pedidos_compra.json"'
    return response

#view importar json

def importar_componentes(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file'].read().decode('utf-8')

        with connection.cursor() as cursor:
            cursor.execute("SELECT importar_componentes(%s)", [json_file])

        return redirect('componente_list')

    return render(request, 'componente/importar_componentes.html')

#view stock componentes

def mostrar_stock_componentes(request):
    with connection.cursor() as cursor:
        # Consulta para obter as entradas de componentes
        cursor.execute('SELECT * FROM entrada_componentes_fornecedor')
        columns = [col[0] for col in cursor.description]
        entradas_componentes = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'componente/stockcomponentes.html', {'entradas_componentes': entradas_componentes})

def mostrar_saida_componentes_folha_de_obra(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM saida_componentes_folha_de_obra')
        saida_componentes = cursor.fetchall()
        print("Saída de componentes:", saida_componentes)

    return render(request, 'componente/saida_componentes_folha_de_obra.html', {'saida_componentes': saida_componentes})

def mostrar_stock_total_componentes(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM stock_componentesfinal')
        total_componentes = cursor.fetchall()
        print("Saída de componentes:", total_componentes)

    return render(request, 'componente/total_componentes.html', {'total_componentes': total_componentes})

def mostrar_stock_componentes_armazem(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM stock_componentes_armazem')
        stock_componentes_armazem = cursor.fetchall()

    return render(request, 'componente/stock_componentes_armazem.html', {'stock_componentes_armazem': stock_componentes_armazem})

def mostrar_entrada_equipamentos(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM entrada_equipamentos_folhadeobra')
        columns = [col[0] for col in cursor.description]
        entradas_equipamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'equipamento/entradas_equipamentos.html', {'entradas_equipamentos': entradas_equipamentos})

def mostrar_saida_equipamentos(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM saida_equipamentos_guia_remessa_cliente')
        columns = [col[0] for col in cursor.description]
        saida_equipamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'equipamento/saida_equipamentos.html', {'saida_equipamentos': saida_equipamentos})

def mostrar_stock_equipamentos(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM stock_equipamentos_final')
        stock_equipamentos = cursor.fetchall()

    return render(request, 'equipamento/stock_equipamentos_final.html', {'stock_equipamentos': stock_equipamentos})

def mostrar_stock_equipamentos_armazem(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM stock_equipamentos_armazem')
        stock_equipamentos_armazem = cursor.fetchall()

    return render(request, 'equipamento/stock_equipamentos_armazem.html', {'stock_equipamentos_armazem': stock_equipamentos_armazem})