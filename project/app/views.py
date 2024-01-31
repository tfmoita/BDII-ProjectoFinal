from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Fornecedor, Cliente, Equipamento, Componente, PedidoComprafornecedor, PedidoCompracliente, FolhaDeObra, DetalhesPedidocompracliente
from .forms import FornecedorForm, ClienteForm, EquipamentoForm, PedidoCompraFornecedorForm, ComponenteForm, FolhaDeObraForm, PedidoDetalhesForm, PedidoCompraClienteForm, DetalhesPedidocomprafornecedorForm
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
                                idequipamento = detalhe_data['idequipamento']
                                quantidade = detalhe_data['quantidade']

                                with connection.cursor() as cursor:
                                    cursor.execute("CALL sp_detalhes_pedidocompracliente_update(%s, %s, %s, %s)",
                                                [pk, idequipamento, quantidade, i + 1])

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

def pedido_comprafornecedor_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fn_listar_pedido_comprafornecedor()')
        columns = [col[0] for col in cursor.description]
        pedidos_compra_fornecedor = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'pedido_comprafornecedor/pedido_comprafornecedor_list.html', {'pedidos_compra_fornecedor': pedidos_compra_fornecedor})

#Pedido compra a fornecedor view

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