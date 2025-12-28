class Empresa:
   
    def __init__(self, nit: str, nombre: str, direccion: str, telefono: str):
        
        self._validar_nit(nit)
        self._validar_nombre(nombre)
        self._validar_direccion(direccion)
        self._validar_telefono(telefono)
        
        self.nit = nit
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
    
    def _validar_nit(self, nit: str) -> None:

        if not nit or not nit.strip():
            raise ValueError("El NIT es requerido")
        if len(nit) > 20:
            raise ValueError("El NIT no puede exceder 20 caracteres")
    
    def _validar_nombre(self, nombre: str) -> None:

        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la empresa es requerido")
        if len(nombre) > 255:
            raise ValueError("El nombre no puede exceder 255 caracteres")
    
    def _validar_direccion(self, direccion: str) -> None:

        if not direccion or not direccion.strip():
            raise ValueError("La dirección es requerida")
        if len(direccion) > 255:
            raise ValueError("La dirección no puede exceder 255 caracteres")
    
    def _validar_telefono(self, telefono: str) -> None:

        if not telefono or not telefono.strip():
            raise ValueError("El teléfono es requerido")
        if len(telefono) > 30:
            raise ValueError("El teléfono no puede exceder 30 caracteres")
    
    def actualizar_nombre(self, nuevo_nombre: str) -> None:

        self._validar_nombre(nuevo_nombre)
        self.nombre = nuevo_nombre
    
    def actualizar_direccion(self, nueva_direccion: str) -> None:

        self._validar_direccion(nueva_direccion)
        self.direccion = nueva_direccion
    
    def actualizar_telefono(self, nuevo_telefono: str) -> None:

        self._validar_telefono(nuevo_telefono)
        self.telefono = nuevo_telefono
    
    def __eq__(self, other) -> bool:

        if not isinstance(other, Empresa):
            return False
        return self.nit == other.nit
    
    def __hash__(self) -> int:

        return hash(self.nit)
    
    def __repr__(self) -> str:

        return f"Empresa(nit='{self.nit}', nombre='{self.nombre}')"

