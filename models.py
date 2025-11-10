"""
Modelos de datos para el Proyecto Trello Manager
Define las clases principales: Usuario, Proyecto, Columna y Tarea
"""

from datetime import datetime
from typing import Optional, List
import uuid


class Usuario:
    """Representa un usuario del sistema"""

    def __init__(self, nombre: str, email: str, usuario_id: Optional[str] = None):
        self.usuario_id = usuario_id or str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.fecha_creacion = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario"""
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "email": self.email,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Crea un usuario desde diccionario"""
        usuario = cls(data["nombre"], data["email"], data["usuario_id"])
        usuario.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        return usuario

    def __repr__(self) -> str:
        return f"Usuario({self.nombre}, {self.email})"


class Tarea:
    """Representa una tarea dentro de una columna"""

    def __init__(
        self,
        titulo: str,
        descripcion: str = "",
        prioridad: str = "Media",
        asignado_a: Optional[str] = None,
        tarea_id: Optional[str] = None,
    ):
        self.tarea_id = tarea_id or str(uuid.uuid4())
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.asignado_a = asignado_a
        self.estado = "Pendiente"
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_modificacion = datetime.now().isoformat()
        self.fecha_vencimiento: Optional[str] = None
        self.etiquetas: List[str] = []

    def actualizar(self, **kwargs):
        """Actualiza atributos de la tarea"""
        permitidos = [
            "titulo",
            "descripcion",
            "prioridad",
            "asignado_a",
            "estado",
            "fecha_vencimiento",
        ]
        for key, value in kwargs.items():
            if key in permitidos:
                setattr(self, key, value)
        self.fecha_modificacion = datetime.now().isoformat()

    def agregar_etiqueta(self, etiqueta: str):
        """Agrega una etiqueta a la tarea"""
        if etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)

    def eliminar_etiqueta(self, etiqueta: str):
        """Elimina una etiqueta de la tarea"""
        if etiqueta in self.etiquetas:
            self.etiquetas.remove(etiqueta)

    def to_dict(self) -> dict:
        """Convierte la tarea a diccionario"""
        return {
            "tarea_id": self.tarea_id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "asignado_a": self.asignado_a,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion,
            "fecha_vencimiento": self.fecha_vencimiento,
            "etiquetas": self.etiquetas,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tarea":
        """Crea una tarea desde diccionario"""
        tarea = cls(
            data["titulo"],
            data.get("descripcion", ""),
            data.get("prioridad", "Media"),
            data.get("asignado_a"),
            data.get("tarea_id"),
        )
        tarea.estado = data.get("estado", "Pendiente")
        tarea.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        tarea.fecha_modificacion = data.get(
            "fecha_modificacion", datetime.now().isoformat()
        )
        tarea.fecha_vencimiento = data.get("fecha_vencimiento")
        tarea.etiquetas = data.get("etiquetas", [])
        return tarea

    def __repr__(self) -> str:
        return f"Tarea({self.titulo}, {self.estado}, {self.prioridad})"


class Columna:
    """Representa una columna en el tablero"""

    def __init__(self, nombre: str, orden: int = 0, columna_id: Optional[str] = None):
        self.columna_id = columna_id or str(uuid.uuid4())
        self.nombre = nombre
        self.orden = orden
        self.tareas: List[Tarea] = []
        self.fecha_creacion = datetime.now().isoformat()

    def agregar_tarea(self, tarea: Tarea) -> bool:
        """Agrega una tarea a la columna"""
        if tarea not in self.tareas:
            self.tareas.append(tarea)
            return True
        return False

    def eliminar_tarea(self, tarea_id: str) -> bool:
        """Elimina una tarea de la columna"""
        for i, tarea in enumerate(self.tareas):
            if tarea.tarea_id == tarea_id:
                self.tareas.pop(i)
                return True
        return False

    def obtener_tarea(self, tarea_id: str) -> Optional[Tarea]:
        """Obtiene una tarea por ID"""
        for tarea in self.tareas:
            if tarea.tarea_id == tarea_id:
                return tarea
        return None

    def listar_tareas(self) -> List[Tarea]:
        """Retorna todas las tareas de la columna"""
        return self.tareas

    def contar_tareas(self) -> int:
        """Cuenta el nÃºmero de tareas"""
        return len(self.tareas)

    def to_dict(self) -> dict:
        """Convierte la columna a diccionario"""
        return {
            "columna_id": self.columna_id,
            "nombre": self.nombre,
            "orden": self.orden,
            "tareas": [tarea.to_dict() for tarea in self.tareas],
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Columna":
        """Crea una columna desde diccionario"""
        columna = cls(data["nombre"], data.get("orden", 0), data.get("columna_id"))
        columna.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        columna.tareas = [Tarea.from_dict(t) for t in data.get("tareas", [])]
        return columna

    def __repr__(self) -> str:
        return f"Columna({self.nombre}, {self.contar_tareas()} tareas)"


class Proyecto:
    """Representa un proyecto con mÃºltiples columnas y tareas"""

    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
        propietario_id: Optional[str] = None,
        proyecto_id: Optional[str] = None,
    ):
        self.proyecto_id = proyecto_id or str(uuid.uuid4())
        self.nombre = nombre
        self.descripcion = descripcion
        self.propietario_id = propietario_id
        self.columnas: List[Columna] = []
        self.miembros: List[str] = []
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_modificacion = datetime.now().isoformat()

    def agregar_columna(self, nombre: str) -> Columna:
        """Agrega una nueva columna al proyecto"""
        orden = len(self.columnas)
        columna = Columna(nombre, orden)
        self.columnas.append(columna)
        self._actualizar_fecha_modificacion()
        return columna

    def eliminar_columna(self, columna_id: str) -> bool:
        """Elimina una columna del proyecto"""
        for i, columna in enumerate(self.columnas):
            if columna.columna_id == columna_id:
                self.columnas.pop(i)
                self._actualizar_fecha_modificacion()
                return True
        return False

    def obtener_columna(self, columna_id: str) -> Optional[Columna]:
        """Obtiene una columna por ID"""
        for columna in self.columnas:
            if columna.columna_id == columna_id:
                return columna
        return None

    def listar_columnas(self) -> List[Columna]:
        """Retorna todas las columnas ordenadas"""
        return sorted(self.columnas, key=lambda c: c.orden)

    def agregar_miembro(self, usuario_id: str) -> bool:
        """Agrega un miembro al proyecto"""
        if usuario_id not in self.miembros:
            self.miembros.append(usuario_id)
            self._actualizar_fecha_modificacion()
            return True
        return False

    def eliminar_miembro(self, usuario_id: str) -> bool:
        """Elimina un miembro del proyecto"""
        if usuario_id in self.miembros:
            self.miembros.remove(usuario_id)
            self._actualizar_fecha_modificacion()
            return True
        return False

    def obtener_todas_las_tareas(self) -> List[Tarea]:
        """Obtiene todas las tareas del proyecto"""
        tareas = []
        for columna in self.columnas:
            tareas.extend(columna.tareas)
        return tareas

    def contar_tareas(self) -> int:
        """Cuenta el nÃºmero total de tareas"""
        return sum(columna.contar_tareas() for columna in self.columnas)

    def _actualizar_fecha_modificacion(self):
        """Actualiza la fecha de modificaciÃ³n"""
        self.fecha_modificacion = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convierte el proyecto a diccionario"""
        return {
            "proyecto_id": self.proyecto_id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "propietario_id": self.propietario_id,
            "columnas": [columna.to_dict() for columna in self.columnas],
            "miembros": self.miembros,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Proyecto":
        """Crea un proyecto desde diccionario"""
        proyecto = cls(
            data["nombre"],
            data.get("descripcion", ""),
            data.get("propietario_id"),
            data.get("proyecto_id"),
        )
        proyecto.columnas = [Columna.from_dict(c) for c in data.get("columnas", [])]
        proyecto.miembros = data.get("miembros", [])
        proyecto.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        proyecto.fecha_modificacion = data.get(
            "fecha_modificacion", datetime.now().isoformat()
        )
        return proyecto

    def __repr__(self) -> str:
        return f"Proyecto({self.nombre}, {len(self.columnas)} columnas, {self.contar_tareas()} tareas)"
