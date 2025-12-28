from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.producto import Producto


class ProductoRepository(ABC):
    
    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        pass
    
    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Producto]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        pass
    
    @abstractmethod
    def listar_por_empresa(self, empresa_nit: str) -> List[Producto]:
        pass
    
    @abstractmethod
    def eliminar(self, codigo: str) -> bool:
        pass
    
    @abstractmethod
    def existe(self, codigo: str) -> bool:
        pass

