from decimal import Decimal
from enum import Enum
from typing import List, Optional


class Moneda(str, Enum):
    """Value Object: Moneda"""
    COP = "COP"
    USD = "USD"
    EUR = "EUR"
    
    @property
    def descripcion(self) -> str:

        descripciones = {
            "COP": "Peso colombiano",
            "USD": "Dólar",
            "EUR": "Euro"
        }
        return descripciones.get(self.value, self.value)


class ProductoPrecio:

    def __init__(self, moneda: Moneda, valor: Decimal):

        self._validar_valor(valor)
        self.moneda = moneda
        self.valor = valor
    
    def _validar_valor(self, valor: Decimal) -> None:

        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        if valor > Decimal('999999999999.99'):
            raise ValueError("El precio excede el valor máximo permitido")
    
    def convertir_a(self, moneda_destino: Moneda, tasa_cambio: Decimal) -> 'ProductoPrecio':
        
        nuevo_valor = self.valor * tasa_cambio
        return ProductoPrecio(moneda_destino, nuevo_valor)
    
    def __eq__(self, other) -> bool:
        """Compara dos precios."""
        if not isinstance(other, ProductoPrecio):
            return False
        return self.moneda == other.moneda and self.valor == other.valor
    
    def __repr__(self) -> str:
        
        return f"ProductoPrecio(moneda={self.moneda.value}, valor={self.valor})"


class Producto:
     
    def __init__(
        self,
        codigo: str,
        nombre: str,
        empresa_nit: str,
        caracteristicas: Optional[str] = None,
        descripcion: Optional[str] = None,
        precios: Optional[List[ProductoPrecio]] = None
    ):
        
        self._validar_codigo(codigo)
        self._validar_nombre(nombre)
        self._validar_empresa_nit(empresa_nit)
        
        self.codigo = codigo
        self.nombre = nombre
        self.empresa_nit = empresa_nit
        self.caracteristicas = caracteristicas or ""
        self.descripcion = descripcion or ""
        self.precios = precios or []
    
    def _validar_codigo(self, codigo: str) -> None:
       
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto es requerido")
        if len(codigo) > 50:
            raise ValueError("El código no puede exceder 50 caracteres")
    
    def _validar_nombre(self, nombre: str) -> None:
        
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto es requerido")
        if len(nombre) > 255:
            raise ValueError("El nombre no puede exceder 255 caracteres")
    
    def _validar_empresa_nit(self, empresa_nit: str) -> None:
       
        if not empresa_nit or not empresa_nit.strip():
            raise ValueError("El NIT de la empresa es requerido")
    
    def agregar_precio(self, precio: ProductoPrecio) -> None:
        
        self.precios = [p for p in self.precios if p.moneda != precio.moneda]
        self.precios.append(precio)
    
    def obtener_precio(self, moneda: Moneda) -> Optional[ProductoPrecio]:
      
        for precio in self.precios:
            if precio.moneda == moneda:
                return precio
        return None
    
    def remover_precio(self, moneda: Moneda) -> None:
       
        self.precios = [p for p in self.precios if p.moneda != moneda]
    
    def actualizar_nombre(self, nuevo_nombre: str) -> None:
        
        self._validar_nombre(nuevo_nombre)
        self.nombre = nuevo_nombre
    
    def actualizar_caracteristicas(self, nuevas_caracteristicas: str) -> None:
        
        self.caracteristicas = nuevas_caracteristicas or ""
    
    def __eq__(self, other) -> bool:
        
        if not isinstance(other, Producto):
            return False
        return self.codigo == other.codigo
    
    def __hash__(self) -> int:
        
        return hash(self.codigo)
    
    def __repr__(self) -> str:
        
        return f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', empresa_nit='{self.empresa_nit}')"

