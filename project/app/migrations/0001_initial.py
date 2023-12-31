# Generated by Django 4.2.7 on 2023-11-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Armazem',
            fields=[
                ('idarmazem', models.AutoField(primary_key=True, serialize=False)),
                ('codigopostal', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'armazem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idcliente', models.AutoField(primary_key=True, serialize=False)),
                ('nomecliente', models.CharField(max_length=100)),
                ('numerotelefonecliente', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('nif', models.IntegerField()),
                ('codigopostal', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('idcomponente', models.AutoField(primary_key=True, serialize=False)),
                ('nomecomponente', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'componente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalhesFolhaDeObra',
            fields=[
                ('quantidade', models.IntegerField()),
                ('iddetalhesfolhadeobra', models.AutoField(primary_key=True, serialize=False)),
                ('datahoradetalhesfolhadeobra', models.DateTimeField()),
            ],
            options={
                'db_table': 'detalhes_folha_de_obra',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalhesGuiaremessacliente',
            fields=[
                ('iddetalhesguiaremessacliente', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('datahoradetalhesguiacliente', models.DateTimeField()),
            ],
            options={
                'db_table': 'detalhes_guiaremessacliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalhesGuiaremessafornecedor',
            fields=[
                ('iddetalhesguiaremessafornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('datahoradetalhesguiafornecedor', models.DateTimeField()),
            ],
            options={
                'db_table': 'detalhes_guiaremessafornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalhesPedidocompracliente',
            fields=[
                ('iddetalhespedidocompracliente', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
            ],
            options={
                'db_table': 'detalhes_pedidocompracliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalhesPedidocomprafornecedor',
            fields=[
                ('iddetalhespedidocomprafornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
            ],
            options={
                'db_table': 'detalhes_pedidocomprafornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('idequipamento', models.AutoField(primary_key=True, serialize=False)),
                ('nomeequipamento', models.CharField(max_length=20)),
                ('descricao', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'equipamento',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Faturacliente',
            fields=[
                ('idfaturacliente', models.AutoField(primary_key=True, serialize=False)),
                ('datahorafaturacliente', models.DateTimeField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'faturacliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Faturafornecedor',
            fields=[
                ('idfaturafornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('datahorafaturafornecedor', models.DateTimeField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'faturafornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FolhaDeObra',
            fields=[
                ('idfolhadeobra', models.AutoField(primary_key=True, serialize=False)),
                ('quantidadeequipamento', models.IntegerField()),
                ('datahorainicio', models.DateTimeField()),
                ('datahorafim', models.DateTimeField()),
                ('precomedio', models.IntegerField()),
            ],
            options={
                'db_table': 'folha_de_obra',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('idfornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('nomefornecedor', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=35)),
                ('numerotelefonefornecedor', models.CharField(max_length=20)),
                ('codigopostal', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'fornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuiaRemessacliente',
            fields=[
                ('idguiaremessacliente', models.AutoField(primary_key=True, serialize=False)),
                ('datahoraguiacliente', models.DateTimeField()),
            ],
            options={
                'db_table': 'guia_remessacliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuiaRemessafornecedor',
            fields=[
                ('idguiaremessafornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('datahoraguiafornecedor', models.DateTimeField()),
            ],
            options={
                'db_table': 'guia_remessafornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MaoDeObra',
            fields=[
                ('idmaodeobra', models.AutoField(primary_key=True, serialize=False)),
                ('tipodemaodeobra', models.CharField(max_length=255)),
                ('custo_hora', models.DecimalField(decimal_places=2, max_digits=10)),
                ('datahoramaodeobra', models.DateTimeField()),
            ],
            options={
                'db_table': 'mao_de_obra',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PedidoCompracliente',
            fields=[
                ('idpedidocompracliente', models.AutoField(primary_key=True, serialize=False)),
                ('datahorapedidocliente', models.DateTimeField()),
                ('preco', models.IntegerField()),
            ],
            options={
                'db_table': 'pedido_compracliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PedidoComprafornecedor',
            fields=[
                ('idpedidocomprafornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('datahorapedidofornecedor', models.DateTimeField()),
                ('preco', models.IntegerField()),
            ],
            options={
                'db_table': 'pedido_comprafornecedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrabalhadorOperario',
            fields=[
                ('idtrabalhadoroperario', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('datacontratacao', models.DateField()),
                ('email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'trabalhador_operario',
                'managed': False,
            },
        ),
    ]
