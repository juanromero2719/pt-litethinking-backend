"""
Módulo de persistencia para Empresa
"""
from .model import EmpresaModel
from .repository_impl import DjangoEmpresaRepository

__all__ = ['EmpresaModel', 'DjangoEmpresaRepository']

