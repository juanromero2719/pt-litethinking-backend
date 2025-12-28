from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaModel',
            fields=[
                ('nit', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='NIT')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre de la empresa')),
                ('direccion', models.CharField(max_length=255, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=30, verbose_name='Teléfono')),
            ],
            options={
                'db_table': 'empresa',
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
    ]

