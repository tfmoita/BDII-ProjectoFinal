# Generated by Django 4.2.7 on 2024-02-08 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_componentepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockComponentePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_stockcomponentes', 'Can view stock componentes')],
            },
        ),
    ]