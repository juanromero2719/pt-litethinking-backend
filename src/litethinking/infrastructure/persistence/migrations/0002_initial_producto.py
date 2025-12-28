import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persistence', '0001_initial_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoModel',
            fields=[
                ('codigo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Código')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre del producto')),
                ('caracteristicas', models.TextField(blank=True, verbose_name='Características')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='persistence.empresamodel')),
            ],
            options={
                'db_table': 'producto',
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='ProductoPrecioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda', models.CharField(choices=[('COP', 'Peso colombiano'), ('USD', 'Dólar'), ('EUR', 'Euro')], max_length=3, verbose_name='Moneda')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Precio')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precios', to='persistence.productomodel')),
            ],
            options={
                'db_table': 'producto_precio',
                'verbose_name': 'Precio de Producto',
                'verbose_name_plural': 'Precios de Productos',
            },
        ),
        migrations.AddConstraint(
            model_name='productopreciomodel',
            constraint=models.UniqueConstraint(fields=('producto', 'moneda'), name='uq_producto_precio__producto_moneda'),
        ),
    ]

