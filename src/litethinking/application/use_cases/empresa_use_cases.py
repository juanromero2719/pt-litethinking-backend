from typing import List, Optional

from ...domain.entities.empresa import Empresa
from ...domain.ports.empresa_repository import EmpresaRepository


class CrearEmpresaUseCase:
    
    def __init__(self, empresa_repository: EmpresaRepository):
        self._empresa_repository = empresa_repository
    
    def ejecutar(self, nit: str, nombre: str, direccion: str, telefono: str) -> Empresa:

        if self._empresa_repository.existe(nit):
            raise ValueError(f"Ya existe una empresa con el NIT: {nit}")
        
        empresa = Empresa(nit=nit, nombre=nombre, direccion=direccion, telefono=telefono)

        return self._empresa_repository.guardar(empresa)


class ObtenerEmpresaUseCase:
    
    def __init__(self, empresa_repository: EmpresaRepository):
        self._empresa_repository = empresa_repository
    
    def ejecutar(self, nit: str) -> Optional[Empresa]:
        return self._empresa_repository.buscar_por_nit(nit)


class ListarEmpresasUseCase:
     
    def __init__(self, empresa_repository: EmpresaRepository):     
        self._empresa_repository = empresa_repository
    
    def ejecutar(self) -> List[Empresa]:
        return self._empresa_repository.listar_todas()


class ActualizarEmpresaUseCase:
  
    def __init__(self, empresa_repository: EmpresaRepository):
        self._empresa_repository = empresa_repository
    
    def ejecutar(
        self,
        nit: str,
        nombre: Optional[str] = None,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None
    ) -> Empresa:

        empresa = self._empresa_repository.buscar_por_nit(nit)
        if not empresa:
            raise ValueError(f"No existe una empresa con el NIT: {nit}")
            
        if nombre is not None:
            empresa.actualizar_nombre(nombre)
        if direccion is not None:
            empresa.actualizar_direccion(direccion)
        if telefono is not None:
            empresa.actualizar_telefono(telefono)
        
        return self._empresa_repository.guardar(empresa)


class EliminarEmpresaUseCase:
   
    def __init__(self, empresa_repository: EmpresaRepository):
        self._empresa_repository = empresa_repository
    
    def ejecutar(self, nit: str) -> bool:
        return self._empresa_repository.eliminar(nit)

