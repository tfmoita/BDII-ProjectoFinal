from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor, PedidoCompracliente, FolhaDeObra, DetalhesPedidocompracliente, Armazem, Faturacliente, GuiaRemessacliente, Faturafornecedor
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm, PedidoDetalhesForm, PedidoCompraClienteForm, DetalhesPedidocomprafornecedorForm, GuiaRemessafornecedorForm, DetalhesGuiaremessafornecedorForm, ArmazemForm, GuiaRemessaclienteForm, DetalhesGuiaremessaclienteForm, FaturaclienteForm, FaturaclienteUpdateForm, FaturafornecedorForm, FaturafornecedorUpdateForm, Folha_de_obraForm, Detalhes_ficha_de_obraForm
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import Http404
from django.db import connection, transaction
from .forms import PedidoCompraClienteForm, PedidoDetalhesForm
from django.forms import formset_factory
import logging

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

            return render(request, 'pedido_compracliente/pedido_compracliente_detail.html', {'pedido_compra_cliente': pedido_compra_cliente})

        raise Http404("Pedido de Compra do Cliente does not exist")

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

    return render(request, 'pedido_compracliente/pedido_compracliente_form.html', {'form_pedido': form_pedido, 'form_detalhes': form_detalhes})




# No seu views.py
def pedido_compracliente_update(request, pk):
    logger = logging.getLogger(__name__)

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_pedido_compracliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])
                row = cursor.fetchone()
                print(f"DEBUG: row: {row}")

                if row is not None and len(row) >= 3:
                    idcliente = row[0]
                    cursor.execute("SELECT nomecliente FROM cliente WHERE idcliente = %s", [idcliente])
                    nomecliente_result = cursor.fetchone()
                    nomecliente = nomecliente_result[0] if nomecliente_result else None

                    cursor.execute("SELECT idequipamento, quantidade FROM detalhes_pedidocompracliente WHERE idpedidocompracliente = %s", [pk])
                    detalhes_pedido_compra_cliente = cursor.fetchall()

                    detalhes_pedido_compra_cliente = [{'idequipamento': detalhe[0], 'quantidade': detalhe[1]} for detalhe in detalhes_pedido_compra_cliente] if detalhes_pedido_compra_cliente else []

                    pedido_compra_cliente_data = {
                        'idcliente': idcliente,
                        'nomecliente': nomecliente,
                        'datahorapedidocliente': row[1] if len(row) > 1 else None,
                        'preco': row[2] if len(row) > 2 else None,
                        'idpedidocompracliente': pk
                    }

                    if 'datahorapedidocliente' in pedido_compra_cliente_data:
                        print("DEBUG datahorapedidocliente exists")
                    else:
                        print("DEBUG datahorapedidocliente does not exist")

                    # Modificação: Verificar se é uma solicitação GET ou POST e inicializar o formulário adequadamente
                    if request.method == 'GET':
                        form_pedido = PedidoCompraClienteForm(initial=pedido_compra_cliente_data)
                    elif request.method == 'POST':
                        form_pedido = PedidoCompraClienteForm(request.POST, initial=pedido_compra_cliente_data)
                    else:
                        raise Http404("Método HTTP não suportado")

                    print(f"form_pedido.errors (POST): {form_pedido.errors}")
                    print(f"form_pedido.is_bound (POST): {form_pedido.is_bound}")
                    print(f"form_pedido.is_valid() (POST): {form_pedido.is_valid()}")

                    # Modificação: Remover o trecho que cria detalhes_forms inicialmente
                    detalhes_forms = []

                    # ...

                   # ...

                    # ...

                    # Adiciona mensagem de depuração para verificar se chegou a este ponto
                    print("DEBUG: Chegou aqui")

                    if form_pedido.is_valid():
                        data_pedido = form_pedido.cleaned_data
                        cliente_id = data_pedido['idcliente']
                        datahorapedido = data_pedido['datahorapedidocliente'] if data_pedido['datahorapedidocliente'] else None

                        # Atualiza o pedido de compra do cliente
                        with connection.cursor() as cursor:
                            cursor.execute("CALL sp_pedido_compracliente_update(%s, %s, %s, %s, %s)",
                                        [pk, cliente_id, datahorapedido, data_pedido['preco']])

                        # Adiciona mensagem de depuração após a atualização do pedido principal
                        print("DEBUG: Pedido de Compra do Cliente atualizado com sucesso")

                        # Recria detalhes_forms apenas se necessário
                        detalhes_forms = []
                        for i, detalhe in enumerate(detalhes_pedido_compra_cliente):
                            prefix = f'detalhe_{i}'
                            try:
                                form = PedidoDetalhesForm(request.POST, prefix=prefix, initial={'idequipamento': detalhe['idequipamento'], 'quantidade': detalhe['quantidade']})
                                detalhes_forms.append(form)
                                print(f"DEBUG: detalhes_forms[{i}] errors: {form.errors}")
                            except Exception as e:
                                print(f"DEBUG: Erro ao criar detalhe form {i}: {e}")

                        # Adiciona mensagem de depuração após a criação dos formulários de detalhes
                        print("DEBUG: Criados formulários de detalhes")

                        if all(form.is_valid() for form in detalhes_forms):
                            for i, form in enumerate(detalhes_forms):
                                detalhe_data = form.cleaned_data
                                idpedidocompracliente = detalhe_data['idpedidocompracliente'] #coloquei isto a mais e no cursor.execute tb
                                idequipamento = detalhe_data['idequipamento']
                                quantidade = detalhe_data['quantidade']

                                with connection.cursor() as cursor:
                                    cursor.execute("CALL sp_detalhes_pedidocompracliente_update(%s, %s, %s, %s, %s)",
                                                [pk, idpedidocompracliente, idequipamento, quantidade, i + 1])

                            logger.info(f"Pedido de Compra do Cliente atualizado com sucesso: {pk}")
                            return redirect('pedido_compracliente_list')
                        else:
                            print(f"DEBUG: Erros nos formulários de detalhes: {[form.errors for form in detalhes_forms]}")
                    else:
                        print(f"DEBUG: Erros no formulário principal: {form_pedido.errors}")

                    # Adiciona mensagem de depuração para verificar se chegou a este ponto em caso de erro
                    print("DEBUG: Chegou aqui após o tratamento de erros")

                    return render(request, 'pedido_compracliente/pedido_compracliente_update_form.html', {'form_pedido': form_pedido, 'detalhes_forms': detalhes_forms, 'action': 'Atualizar', 'detalhes_pedido_compra_cliente': detalhes_pedido_compra_cliente})



                else:
                    raise Http404("Pedido de Compra do Cliente does not exist")

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        logger.error(f"Erro ao processar a solicitação: {e}")
        raise Http404("Erro ao processar a solicitação")

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

    return render(request, 'pedido_compracliente/pedido_compracliente_confirm_delete.html', {'idpedidocompracliente': pk})

#Pedido compra a fornecedor view

def pedido_comprafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_pedido_comprafornecedor()')
        columns = [col[0] for col in cursor.description]
        pedidos_compra_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_list.html', {'pedidos_compra_fornecedor': pedidos_compra_fornecedor})


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

            return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_detail.html', {'pedido_compra_fornecedor': pedido_compra_fornecedor})

        raise Http404("Pedido de Compra do Fornecedor does not exist")
    
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

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_form.html', {'form_pedido': form_pedido, 'form_detalhes': form_detalhes})

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

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_confirm_delete.html', {'idpedidocomprafornecedor': pk})

# views da guia de remessa do fornecedor

def guia_remessafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_guia_remessafornecedor()')
        columns = [col[0] for col in cursor.description]
        guias_remessa_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_list.html', {'guias_remessa_fornecedor': guias_remessa_fornecedor})

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
            

            return render(request, 'guia_remessafornecedor/guia_remessafornecedor_detail.html', {'guia_remessa_fornecedor': guia_remessa_fornecedor})

        raise Http404("Guia de Remessa para Fornecedor does not exist")

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

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_form.html', {'form_guia_remessa': form_guia_remessa, 'form_detalhes': form_detalhes})

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

    return render(request, 'guia_remessafornecedor/guia_remessafornecedor_confirm_delete.html', {'idguiaremessafornecedor': pk})

# views do armazem

def armazem_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_armazem()')
        columns = [col[0] for col in cursor.description]
        armazens = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'armazem/armazem_list.html', {'armazens': armazens})

def armazem_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_armazem_read(%s, %s)", [pk, ''])
        row = cursor.fetchone()

        if row:
            armazem = {
                'codigopostal': row[0],
                'idarmazem': pk
            }
            return render(request, 'armazem/armazem_detail.html', {'armazem': armazem})

        raise Http404("Armazem does not exist")
    
def armazem_create(request):
    form = ArmazemForm()

    if request.method == 'POST':
        form = ArmazemForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("CALL sp_armazem_create(%s)", [data['codigopostal']])
            return redirect('armazem_list')

    return render(request, 'armazem/armazem_form.html', {'form': form})

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
                    return render(request, 'armazem/armazem_form.html', {'form': form, 'action': 'Atualizar'})
            else:
                raise Http404("Armazém does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
def armazem_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_armazem_read(%s, %s)", [pk, ''])
            row = cursor.fetchone()

            if row:
                armazem = get_object_or_404(Armazem, pk=pk)  # Certifique-se de importar o modelo Armazem
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_armazem_delete(%s)", [pk])
                    return redirect('armazem_list')
                else:
                    return render(request, 'armazem/armazem_confirm_delete.html', {'armazem': armazem})
            else:
                raise Http404("Armazém does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#views da guia de remessa ao cliente
    
def guia_remessacliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_guia_remessacliente()')
        columns = [col[0] for col in cursor.description]
        guias_remessa_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'guia_remessacliente/guia_remessacliente_list.html', {'guias_remessa_cliente': guias_remessa_cliente})


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

            return render(request, 'guia_remessacliente/guia_remessacliente_detail.html', {'guia_remessa_cliente': guia_remessa_cliente})

        raise Http404("Guia de Remessa para Cliente does not exist")


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

    return render(request, 'guia_remessacliente/guia_remessacliente_form.html', {'form_guia_remessa': form_guia_remessa, 'form_detalhes': form_detalhes})

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

    return render(request, 'guia_remessacliente/guia_remessacliente_confirm_delete.html', {'idguiaremessacliente': pk})

def faturacliente_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_faturacliente()')
        columns = [col[0] for col in cursor.description]
        faturas_cliente = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(faturas_cliente)  # Adicione este print para verificar os dados na console do servidor

    return render(request, 'faturacliente/faturacliente_list.html', {'faturaclientes': faturas_cliente})


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



def faturacliente_update(request, pk):
    fatura = get_object_or_404(Faturacliente, pk=pk)

    if request.method == 'POST':
        form_fatura = FaturaclienteUpdateForm(request.POST)

        if form_fatura.is_valid():
            with transaction.atomic():
                # Atualizar a fatura do cliente
                data_fatura = form_fatura.cleaned_data
                idguiaremessacliente = data_fatura.get('idguiaremessacliente', None)

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_faturacliente_update(%s, %s, %s, %s)", [
                        fatura.pk, idguiaremessacliente, data_fatura['datahorafaturacliente'], data_fatura['preco']
                    ])

            return redirect('faturacliente_list')  # Redirecionar para a lista de faturas
    else:
        form_fatura = FaturaclienteUpdateForm(instance=fatura)

    return render(request, 'faturacliente/faturacliente_form_update.html', {'form_fatura': form_fatura})



    
def faturacliente_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_faturacliente_read(%s, %s, %s, %s)", [pk, 0, None, 0])  # Ajuste conforme necessário
            row = cursor.fetchone()

            if row:
                faturacliente = get_object_or_404(Faturacliente, pk=pk)
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_faturacliente_delete(%s)", [pk])
                    return redirect('faturacliente_list')
                else:
                    return render(request, 'faturacliente/faturacliente_confirm_delete.html', {'faturacliente': faturacliente})
            else:
                raise Http404("Fatura do Cliente does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
def faturafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_faturafornecedor()')
        columns = [col[0] for col in cursor.description]
        faturas_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(faturas_fornecedor)  # Adicione esta linha para imprimir os dados no console
    
    return render(request, 'faturafornecedor/faturafornecedor_list.html', {'faturafornecedores': faturas_fornecedor})


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

            return render(request, 'faturafornecedor/faturafornecedor_detail.html', {'faturafornecedor': fatura_fornecedor})

        raise Http404("Fatura do Fornecedor does not exist")

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

    return render(request, 'faturafornecedor/faturafornecedor_form.html', {'form_fatura': form_fatura})

def faturafornecedor_update(request, pk):
    fatura = get_object_or_404(Faturafornecedor, pk=pk)

    if request.method == 'POST':
        form_fatura = FaturafornecedorUpdateForm(request.POST, instance=fatura)

        if form_fatura.is_valid():
            with transaction.atomic():
                # Atualizar a fatura do fornecedor
                data_fatura = form_fatura.cleaned_data
                idguiaremessafornecedor = data_fatura.get('idguiaremessafornecedor', None)

                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_faturafornecedor_update(%s, %s, %s, %s)", [
                        fatura.pk, idguiaremessafornecedor, data_fatura['datahorafaturafornecedor'], data_fatura['preco']
                    ])

            return redirect('faturafornecedor_list')  # Redirecionar para a lista de faturas de fornecedor
    else:
        form_fatura = FaturafornecedorUpdateForm(instance=fatura)

    return render(request, 'faturafornecedor/faturafornecedor_form_update.html', {'form_fatura': form_fatura})

def faturafornecedor_delete(request, pk):
    try:
        with connection.cursor() as cursor:
            # Ajuste conforme necessário para a sua implementação
            cursor.execute("CALL sp_faturafornecedor_read(%s, %s, %s, %s)", [pk, 0, None, 0])
            row = cursor.fetchone()

            if row:
                faturafornecedor = get_object_or_404(Faturafornecedor, pk=pk)  # Certifique-se de importar o modelo correto
                if request.method == 'POST':
                    with connection.cursor() as delete_cursor:
                        delete_cursor.execute("CALL sp_faturafornecedor_delete(%s)", [pk])
                    return redirect('faturafornecedor_list')
                else:
                    return render(request, 'faturafornecedor/faturafornecedor_confirm_delete.html', {'faturafornecedor': faturafornecedor})
            else:
                raise Http404("Fatura do Fornecedor does not exist")

    except Exception as e:
        print(e)
        raise Http404("Erro ao processar a solicitação")
    
#folha de obra views

def folha_de_obra_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_folha_de_obra()')
        columns = [col[0] for col in cursor.description]
        folhas_de_obra = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'folha_de_obra/folha_de_obra_list.html', {'folhas_de_obra': folhas_de_obra})

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

            return render(request, 'folha_de_obra/folha_de_obra_detail.html', {'folha_de_obra': folha_de_obra})

        raise Http404("Folha de Obra does not exist")
    
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

    return render(request, 'folha_de_obra/folha_de_obra_form.html', {'form_folha_obra': form_folha_obra, 'form_detalhes': form_detalhes})

def folha_de_obra_delete(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Chame o procedimento armazenado para deletar os detalhes da folha de obra
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_detalhes_ficha_de_obra_delete(%s)", [pk])

                # Chame o procedimento armazenado para deletar a folha de obra
                with connection.cursor() as cursor:
                    cursor.execute("CALL sp_folha_de_obra_delete(%s)", [pk])

                return redirect('folha_de_obra_list')

        except Exception as e:
            print(f"Erro ao processar a solicitação: {e}")
            raise Http404("Erro ao processar a solicitação")

    return render(request, 'folha_de_obra/folha_de_obra_confirm_delete.html', {'idfolhadeobra': pk})