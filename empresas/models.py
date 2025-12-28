from django.db import models

# Create your models here.

class Empresa(models.Model):
    nit = models.CharField("NIT", max_length=20, primary_key=True)
    nombre = models.CharField("Nombre de la empresa", max_length=255)
    direccion = models.CharField("Dirección", max_length=255)
    telefono = models.CharField("Teléfono", max_length=30)

    class Meta:
        db_table = "empresa"

    def __str__(self):
        return f"{self.nombre} ({self.nit})"