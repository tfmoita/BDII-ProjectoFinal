# forms.py
from django import forms
from .models import Fornecedor, Cliente, Equipamento, PedidoComprafornecedor, Componente, PedidoCompracliente, FolhaDeObra, TrabalhadorOperario, Armazem, DetalhesPedidocompracliente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import connection

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        labels = {
            'nomefornecedor': 'Nome do Fornecedor',
            'email': 'Endereço de Email',
            'numerotelefonefornecedor': 'Número de Telefone',
            'codigopostal': 'Código Postal',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'nomecliente': 'Nome',
            'numerotelefonecliente': 'Número de Telefone',
            'email': 'Endereço de Email',
            'nif': 'NIF',
            'codigopostal': 'Código Postal',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'
        labels = {
            'nomeequipamento': 'Nome do Equipamento',
            'descricao': 'Descrição',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))
        
class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = '__all__'
        labels = {
            'nomecomponente': 'Nome do Componente',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

class PedidoCompraFornecedorForm(forms.ModelForm):
    class Meta:
        model = PedidoComprafornecedor
        fields = '__all__'
        labels = {
            'idfornecedor': 'Fornecedor',
            'datahorapedidofornecedor': 'Data e Hora do Pedido',
            'preco': 'Preço',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

class PedidoCompraClienteForm(forms.Form):
    # Lógica para obter a lista de clientes usando SQL puro
    clientes_query = "SELECT idcliente, nomecliente FROM cliente"
    with connection.cursor() as cursor:
        cursor.execute(clientes_query)
        clientes = cursor.fetchall()

    # Criar lista de tuplas (idcliente, nomecliente) para usar como choices
    clientes_choices = [(cliente[0], cliente[1]) for cliente in clientes]

    # Inicializar o campo datahorapedidocliente de forma mais segura
    datahorapedidocliente = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)

    idcliente = forms.ChoiceField(choices=clientes_choices, label='Nome do Cliente')
    preco = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        datahorapedido = cleaned_data.get('datahorapedidocliente')

        if datahorapedido:
            cleaned_data['datahorapedidocliente'] = datahorapedido.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            cleaned_data['datahorapedidocliente'] = None

        return cleaned_data


class PedidoDetalhesForm(forms.ModelForm):
    class Meta:
        model = DetalhesPedidocompracliente
        fields = ['idequipamento', 'quantidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Lógica para obter a lista de equipamentos usando SQL puro
        equipamentos_query = "SELECT idequipamento, nomeequipamento FROM equipamento"
        with connection.cursor() as cursor:
            cursor.execute(equipamentos_query)
            equipamentos = cursor.fetchall()

        # Criar lista de tuplas (idequipamento, nomeequipamento) para usar como choices
        equipamentos_choices = [(str(equipamento[0]), equipamento[1]) for equipamento in equipamentos]

        # Atualizar o campo idequipamento com as escolhas e o widget Select
        self.fields['idequipamento'].choices = equipamentos_choices
        self.fields['idequipamento'].widget = forms.Select(choices=equipamentos_choices)


class PedidoCompraFornecedorForm(forms.Form):
    # Lógica para obter a lista de fornecedores usando SQL puro
    fornecedores_query = "SELECT idfornecedor, nomefornecedor FROM fornecedor"
    with connection.cursor() as cursor:
        cursor.execute(fornecedores_query)
        fornecedores = cursor.fetchall()

    # Criar lista de tuplas (idfornecedor, nomefornecedor) para usar como choices
    fornecedores_choices = [(fornecedor[0], fornecedor[1]) for fornecedor in fornecedores]

    datahorapedidofornecedor = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    idfornecedor = forms.ChoiceField(choices=fornecedores_choices, label='Nome do Fornecedor')
    preco = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        datahorapedido = cleaned_data.get('datahorapedidofornecedor')

        if datahorapedido:
            cleaned_data['datahorapedidofornecedor'] = datahorapedido.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            cleaned_data['datahorapedidofornecedor'] = None

        return cleaned_data

# DetalhesPedidocomprafornecedorForm
class DetalhesPedidocomprafornecedorForm(forms.Form):
    idcomponente = forms.IntegerField()
    quantidade = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Lógica para obter dinamicamente a lista de componentes (ou equipamentos do fornecedor)
        componentes_query = "SELECT idcomponente, nomecomponente FROM componente"
        with connection.cursor() as cursor:
            cursor.execute(componentes_query)
            componentes = cursor.fetchall()

        # Criar lista de tuplas (idcomponente, nomecomponente) para usar como choices
        componentes_choices = [(str(componente[0]), componente[1]) for componente in componentes]

        # Adicionar choices ao campo idcomponente
        self.fields['idcomponente'] = forms.ChoiceField(choices=componentes_choices, label='Componente')


class FolhaDeObraForm(forms.ModelForm):
    class Meta:
        model = FolhaDeObra
        fields = '__all__'
        labels = {
            'idmaodeobra': 'Mão de Obra',
            'idequipamento': 'Equipamento',
            'quantidadeequipamento': 'Quantidade de Equipamento',
            'datahorainicio': 'Data e Hora de Início',
            'datahorafim': 'Data e Hora de Fim',
            'idarmazem': 'Armazém',
            'precomedio': 'Preço Médio',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))
        
