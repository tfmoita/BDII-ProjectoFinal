# Generated by Django 4.2.7 on 2024-02-08 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_stockcomponentepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockEquipamentoPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_stockequipamentos', 'Can view stock equipamentos')],
            },
        ),
    ]
