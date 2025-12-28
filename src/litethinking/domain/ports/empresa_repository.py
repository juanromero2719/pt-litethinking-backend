from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.empresa import Empresa


class EmpresaRepository(ABC):
    
    @abstractmethod
    def guardar(self, empresa: Empresa) -> Empresa:
        pass
    
    @abstractmethod
    def buscar_por_nit(self, nit: str) -> Optional[Empresa]:
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Empresa]:
        pass
    
    @abstractmethod
    def eliminar(self, nit: str) -> bool:
        pass
    
    @abstractmethod
    def existe(self, nit: str) -> bool:
        pass

