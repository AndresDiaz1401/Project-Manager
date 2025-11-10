"""
MÃ³dulo de persistencia de datos
Maneja la carga y guardado de proyectos en JSON
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

from models import Proyecto, Usuario
from config import DATA_FILE


class StorageManager:
    """Gestiona la persistencia de datos en JSON"""

    def __init__(self, archivo_datos: Path = DATA_FILE):
        self.archivo_datos = archivo_datos
        self.archivo_datos.parent.mkdir(parents=True, exist_ok=True)

    def cargar_datos(self) -> Dict:
        """Carga todos los datos del archivo JSON"""
        if self.archivo_datos.exists():
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar datos: {e}")
                return {"proyectos": [], "usuarios": []}
        return {"proyectos": [], "usuarios": []}

    def guardar_datos(self, datos: Dict) -> bool:
        """Guarda todos los datos en el archivo JSON"""
        try:
            with open(self.archivo_datos, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar datos: {e}")
            return False

    def cargar_proyecto(self, proyecto_id: str) -> Optional[Proyecto]:
        """Carga un proyecto especÃ­fico"""
        datos = self.cargar_datos()
        for datos_proyecto in datos.get("proyectos", []):
            if datos_proyecto["proyecto_id"] == proyecto_id:
                return Proyecto.from_dict(datos_proyecto)
        return None

    def guardar_proyecto(self, proyecto: Proyecto) -> bool:
        """Guarda un proyecto"""
        datos = self.cargar_datos()

        # Buscar y actualizar o crear
        proyectos = datos.get("proyectos", [])
        for i, p in enumerate(proyectos):
            if p["proyecto_id"] == proyecto.proyecto_id:
                proyectos[i] = proyecto.to_dict()
                datos["proyectos"] = proyectos
                return self.guardar_datos(datos)

        # Si no existe, agregarlo
        proyectos.append(proyecto.to_dict())
        datos["proyectos"] = proyectos
        return self.guardar_datos(datos)

    def cargar_todos_proyectos(self) -> List[Proyecto]:
        """Carga todos los proyectos"""
        datos = self.cargar_datos()
        proyectos = []
        for datos_proyecto in datos.get("proyectos", []):
            proyectos.append(Proyecto.from_dict(datos_proyecto))
        return proyectos

    def eliminar_proyecto(self, proyecto_id: str) -> bool:
        """Elimina un proyecto"""
        datos = self.cargar_datos()
        proyectos = datos.get("proyectos", [])
        datos["proyectos"] = proyectos
        return self.guardar_datos(datos)

    def cargar_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """Carga un usuario especÃ­fico"""
        datos = self.cargar_datos()
        for datos_usuario in datos.get("usuarios", []):
            if datos_usuario["usuario_id"] == usuario_id:
                return Usuario.from_dict(datos_usuario)
        return None

    def guardar_usuario(self, usuario: Usuario) -> bool:
        """Guarda un usuario"""
        datos = self.cargar_datos()

        # Buscar y actualizar o crear
        usuarios = datos.get("usuarios", [])
        for i, u in enumerate(usuarios):
            if u["usuario_id"] == usuario.usuario_id:
                usuarios[i] = usuario.to_dict()
                datos["usuarios"] = usuarios
                return self.guardar_datos(datos)

        # Si no existe, agregarlo
        usuarios.append(usuario.to_dict())
        datos["usuarios"] = usuarios
        return self.guardar_datos(datos)

    def cargar_todos_usuarios(self) -> List[Usuario]:
        """Carga todos los usuarios"""
        datos = self.cargar_datos()
        usuarios = []
        for datos_usuario in datos.get("usuarios", []):
            usuarios.append(Usuario.from_dict(datos_usuario))
        return usuarios

    def eliminar_usuario(self, usuario_id: str) -> bool:
        """Elimina un usuario"""
        datos = self.cargar_datos()
        usuarios = datos.get("usuarios", [])
        datos["usuarios"] = [u for u in usuarios if u["usuario_id"] != usuario_id]
        return self.guardar_datos(datos)
