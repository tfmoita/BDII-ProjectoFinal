# forms.py
from django import forms
from .models import Fornecedor, Cliente, Equipamento, PedidoComprafornecedor, Componente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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


