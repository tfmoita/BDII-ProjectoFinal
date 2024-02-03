from django.db import models


class Armazem(models.Model):
    idarmazem = models.AutoField(primary_key=True)
    codigopostal = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'armazem'


class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    nomecliente = models.CharField(max_length=100)
    numerotelefonecliente = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    nif = models.IntegerField()
    codigopostal = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cliente'


class Componente(models.Model):
    idcomponente = models.AutoField(primary_key=True)
    nomecomponente = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'componente'


class DetalhesFolhaDeObra(models.Model):
    idfolhadeobra = models.ForeignKey('FolhaDeObra', models.DO_NOTHING, db_column='idfolhadeobra')
    idcomponente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='idcomponente')
    quantidade = models.IntegerField()
    idarmazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='idarmazem')
    iddetalhesfolhadeobra = models.AutoField(primary_key=True)
    datahoradetalhesfolhadeobra = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'detalhes_folha_de_obra'


class DetalhesGuiaremessacliente(models.Model):
    iddetalhesguiaremessacliente = models.AutoField(primary_key=True)
    idarmazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='idarmazem')
    idguiaremessacliente = models.ForeignKey('GuiaRemessacliente', models.DO_NOTHING, db_column='idguiaremessacliente')
    quantidade = models.IntegerField()
    idequipamento = models.ForeignKey('Equipamento', models.DO_NOTHING, db_column='idequipamento')
    datahoradetalhesguiacliente = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'detalhes_guiaremessacliente'


class DetalhesGuiaremessafornecedor(models.Model):
    iddetalhesguiaremessafornecedor = models.AutoField(primary_key=True)
    idarmazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='idarmazem')
    idguiaremessafornecedor = models.ForeignKey('GuiaRemessafornecedor', models.DO_NOTHING, db_column='idguiaremessafornecedor')
    idcomponente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='idcomponente')
    quantidade = models.IntegerField()
    datahoradetalhesguiafornecedor = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'detalhes_guiaremessafornecedor'


class DetalhesPedidocompracliente(models.Model):
    iddetalhespedidocompracliente = models.AutoField(primary_key=True)
    idpedidocompracliente = models.ForeignKey('PedidoCompracliente', models.DO_NOTHING, db_column='idpedidocompracliente')
    idequipamento = models.IntegerField()
    quantidade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalhes_pedidocompracliente'


class DetalhesPedidocomprafornecedor(models.Model):
    iddetalhespedidocomprafornecedor = models.AutoField(primary_key=True)
    idpedidocomprafornecedor = models.ForeignKey('PedidoComprafornecedor', models.DO_NOTHING, db_column='idpedidocomprafornecedor')
    idcomponente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='idcomponente')
    quantidade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalhes_pedidocomprafornecedor'


class Equipamento(models.Model):
    idequipamento = models.AutoField(primary_key=True)
    nomeequipamento = models.CharField(max_length=20)
    descricao = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'equipamento'


class Faturacliente(models.Model):
    idfaturacliente = models.AutoField(primary_key=True)
    idguiaremessacliente = models.ForeignKey('GuiaRemessacliente', models.DO_NOTHING, db_column='idguiaremessacliente')
    datahorafaturacliente = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'faturacliente'


class Faturafornecedor(models.Model):
    idfaturafornecedor = models.AutoField(primary_key=True)
    idguiaremessafornecedor = models.ForeignKey('GuiaRemessafornecedor', models.DO_NOTHING, db_column='idguiaremessafornecedor')
    datahorafaturafornecedor = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'faturafornecedor'


class FolhaDeObra(models.Model):
    idfolhadeobra = models.AutoField(primary_key=True)
    idmaodeobra = models.ForeignKey('MaoDeObra', models.DO_NOTHING, db_column='idmaodeobra')
    idequipamento = models.ForeignKey(Equipamento, models.DO_NOTHING, db_column='idequipamento')
    quantidadeequipamento = models.IntegerField()
    datahorainicio = models.DateTimeField()
    datahorafim = models.DateTimeField()
    idarmazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='idarmazem')
    precomedio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'folha_de_obra'


class Fornecedor(models.Model):
    idfornecedor = models.AutoField(primary_key=True)
    nomefornecedor = models.CharField(max_length=255)
    email = models.CharField(max_length=35)
    numerotelefonefornecedor = models.CharField(max_length=20)
    codigopostal = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'fornecedor'


class GuiaRemessacliente(models.Model):
    idguiaremessacliente = models.AutoField(primary_key=True)
    idpedidocompracliente = models.ForeignKey('PedidoCompracliente', models.DO_NOTHING, db_column='idpedidocompracliente')
    datahoraguiacliente = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guia_remessacliente'


class GuiaRemessafornecedor(models.Model):
    idguiaremessafornecedor = models.AutoField(primary_key=True)
    idpedidocomprafornecedor = models.ForeignKey('PedidoComprafornecedor', models.DO_NOTHING, db_column='idpedidocomprafornecedor')
    datahoraguiafornecedor = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guia_remessafornecedor'


class MaoDeObra(models.Model):
    idmaodeobra = models.AutoField(primary_key=True)
    idtrabalhadoroperario = models.ForeignKey('TrabalhadorOperario', models.DO_NOTHING, db_column='idtrabalhadoroperario')
    tipodemaodeobra = models.CharField(max_length=255)
    custo_hora = models.DecimalField(max_digits=10, decimal_places=2)
    datahoramaodeobra = models.DateTimeField()
    idequipamento = models.ForeignKey(Equipamento, models.DO_NOTHING, db_column='idequipamento')

    class Meta:
        managed = False
        db_table = 'mao_de_obra'


class PedidoCompracliente(models.Model):
    idpedidocompracliente = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='idcliente')
    datahorapedidocliente = models.DateTimeField()
    preco = models.IntegerField()


    class Meta: 
        managed = False
        db_table = 'pedido_compracliente'



class PedidoComprafornecedor(models.Model):
    idpedidocomprafornecedor = models.AutoField(primary_key=True)
    idfornecedor = models.ForeignKey(Fornecedor, models.DO_NOTHING, db_column='idfornecedor')
    datahorapedidofornecedor = models.DateTimeField()
    preco = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pedido_comprafornecedor'


class TrabalhadorOperario(models.Model):
    idtrabalhadoroperario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    datacontratacao = models.DateField()
    email = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'trabalhador_operario'