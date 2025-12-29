from typing import List, Optional

from ....domain.entities.empresa import Empresa
from ....domain.ports.empresa_repository import EmpresaRepository
from .model import EmpresaModel


class DjangoEmpresaRepository(EmpresaRepository):

    def guardar(self, empresa: Empresa) -> Empresa:

        empresa_model, created = EmpresaModel.objects.update_or_create(
            nit=empresa.nit,
            defaults={
                'nombre': empresa.nombre,
                'direccion': empresa.direccion,
                'telefono': empresa.telefono,
            }
        )
     
        empresa_model.refresh_from_db()
        return self._to_domain_entity(empresa_model)
    
    def buscar_por_nit(self, nit: str) -> Optional[Empresa]:
        try:
            empresa_model = EmpresaModel.objects.get(nit=nit)
            return self._to_domain_entity(empresa_model)
        except EmpresaModel.DoesNotExist:
            return None
    
    def listar_todas(self) -> List[Empresa]:
        empresas_model = EmpresaModel.objects.all()
        return [self._to_domain_entity(emp) for emp in empresas_model]
    
    def eliminar(self, nit: str) -> bool:
        try:
            empresa_model = EmpresaModel.objects.get(nit=nit)
            empresa_model.delete()
            return True
        except EmpresaModel.DoesNotExist:
            return False
        except Exception as e:
            raise
    
    def existe(self, nit: str) -> bool:
        return EmpresaModel.objects.filter(nit=nit).exists()
    
    def _to_domain_entity(self, empresa_model: EmpresaModel) -> Empresa:
        return Empresa(
            nit=empresa_model.nit,
            nombre=empresa_model.nombre,
            direccion=empresa_model.direccion,
            telefono=empresa_model.telefono
        )

