"""
MÃ³dulo de utilidades
Funciones auxiliares para el proyecto
"""

from typing import List
from datetime import datetime, timedelta
from models import Proyecto, Tarea


class ProyectoAnalytics:
    """AnÃ¡lisis y generaciÃ³n de reportes de proyectos"""

    @staticmethod
    def obtener_tareas_por_prioridad(proyecto: Proyecto) -> dict:
        """Retorna el conteo de tareas por prioridad"""
        tareas = proyecto.obtener_todas_las_tareas()
        prioridades = {"Baja": 0, "Media": 0, "Alta": 0, "Urgente": 0}
        for tarea in tareas:
            if tarea.prioridad in prioridades:
                prioridades[tarea.prioridad] += 1
        return prioridades

    @staticmethod
    def obtener_tareas_por_estado(proyecto: Proyecto) -> dict:
        """Retorna el conteo de tareas por estado"""
        tareas = proyecto.obtener_todas_las_tareas()
        estados = {"Pendiente": 0, "En Progreso": 0, "Completada": 0, "Bloqueada": 0}
        for tarea in tareas:
            if tarea.estado in estados:
                estados[tarea.estado] += 1
        return estados

    @staticmethod
    def obtener_tareas_por_usuario(proyecto: Proyecto) -> dict:
        """Retorna el conteo de tareas asignadas por usuario"""
        tareas = proyecto.obtener_todas_las_tareas()
        usuarios = {}
        sin_asignar = 0

        for tarea in tareas:
            if tarea.asignado_a:
                usuarios[tarea.asignado_a] = usuarios.get(tarea.asignado_a, 0) + 1
            else:
                sin_asignar += 1

        usuarios["Sin Asignar"] = sin_asignar
        return usuarios

    @staticmethod
    def obtener_tareas_retrasadas(proyecto: Proyecto) -> List[Tarea]:
        """Retorna tareas con fecha de vencimiento pasada"""
        tareas = proyecto.obtener_todas_las_tareas()
        retrasadas = []
        hoy = datetime.now().date()

        for tarea in tareas:
            if tarea.fecha_vencimiento:
                try:
                    fecha_venc = datetime.fromisoformat(tarea.fecha_vencimiento).date()
                    if fecha_venc < hoy and tarea.estado != "Completada":
                        retrasadas.append(tarea)
                except (ValueError, TypeError):
                    pass

        return retrasadas

    @staticmethod
    def obtener_progreso_proyecto(proyecto: Proyecto) -> float:
        """Retorna el porcentaje de progreso del proyecto (0-100)"""
        tareas = proyecto.obtener_todas_las_tareas()
        if not tareas:
            return 0.0

        completadas = sum(1 for t in tareas if t.estado == "Completada")
        return (completadas / len(tareas)) * 100

    @staticmethod
    def generar_reporte_texto(proyecto: Proyecto) -> str:
        """Genera un reporte de texto del proyecto"""
        reporte = []
        reporte.append(f"\n{'='*60}")
        reporte.append(f"REPORTE DE PROYECTO: {proyecto.nombre}")
        reporte.append(f"{'='*60}\n")

        reporte.append(f"DescripciÃ³n: {proyecto.descripcion}")
        reporte.append(f"Creado: {proyecto.fecha_creacion}")
        reporte.append(f"Modificado: {proyecto.fecha_modificacion}")
        reporte.append("")

        # EstadÃ­sticas generales
        reporte.append("ESTADÃSTICAS GENERALES:")
        reporte.append(f"  Total de tareas: {proyecto.contar_tareas()}")
        reporte.append(f"  Total de columnas: {len(proyecto.columnas)}")
        reporte.append(
            f"  Progreso: {ProyectoAnalytics.obtener_progreso_proyecto(proyecto):.1f}%"
        )
        reporte.append("")

        # Por estado
        reporte.append("POR ESTADO:")
        estados = ProyectoAnalytics.obtener_tareas_por_estado(proyecto)
        for estado, count in estados.items():
            reporte.append(f"  {estado}: {count}")
        reporte.append("")

        # Por prioridad
        reporte.append("POR PRIORIDAD:")
        prioridades = ProyectoAnalytics.obtener_tareas_por_prioridad(proyecto)
        for prioridad, count in prioridades.items():
            reporte.append(f"  {prioridad}: {count}")
        reporte.append("")

        # Por usuario
        reporte.append("ASIGNACIÃ“N DE TAREAS:")
        usuarios = ProyectoAnalytics.obtener_tareas_por_usuario(proyecto)
        for usuario, count in usuarios.items():
            reporte.append(f"  {usuario}: {count}")
        reporte.append("")

        # Tareas retrasadas
        retrasadas = ProyectoAnalytics.obtener_tareas_retrasadas(proyecto)
        if retrasadas:
            reporte.append("âš ï¸  TAREAS RETRASADAS:")
            for tarea in retrasadas:
                reporte.append(f"  - {tarea.titulo} (vence: {tarea.fecha_vencimiento})")
            reporte.append("")

        # Por columna
        reporte.append("DISTRIBUCIÃ“N POR COLUMNA:")
        for columna in proyecto.listar_columnas():
            reporte.append(f"  {columna.nombre}:")
            for tarea in columna.tareas:
                reporte.append(f"    â€¢ {tarea.titulo} [{tarea.prioridad}]")

        reporte.append(f"\n{'='*60}\n")

        return "\n".join(reporte)


class ValidadorDatos:
    """ValidaciÃ³n de datos y entrada"""

    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato de email"""
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def validar_prioridad(prioridad: str) -> bool:
        """Valida que la prioridad sea vÃ¡lida"""
        validas = ["Baja", "Media", "Alta", "Urgente"]
        return prioridad in validas

    @staticmethod
    def validar_estado(estado: str) -> bool:
        """Valida que el estado sea vÃ¡lido"""
        validos = ["Pendiente", "En Progreso", "Completada", "Bloqueada"]
        return estado in validos

    @staticmethod
    def validar_no_vacio(texto: str) -> bool:
        """Valida que el texto no estÃ© vacÃ­o"""
        return texto.strip() != ""

    @staticmethod
    def validar_fecha_iso(fecha: str) -> bool:
        """Valida que la fecha estÃ© en formato ISO"""
        try:
            datetime.fromisoformat(fecha)
            return True
        except (ValueError, TypeError):
            return False


class ExportadorDatos:
    """Exporta datos del proyecto a diferentes formatos"""

    @staticmethod
    def exportar_a_json_simple(proyecto: Proyecto) -> dict:
        """Exporta proyecto a diccionario JSON"""
        return proyecto.to_dict()

    @staticmethod
    def exportar_a_csv(proyecto: Proyecto) -> str:
        """Exporta tareas del proyecto a formato CSV"""
        tareas = proyecto.obtener_todas_las_tareas()

        lineas = []
        lineas.append(
            "ID Tarea,TÃ­tulo,DescripciÃ³n,Prioridad,Estado,Asignado A,Fecha CreaciÃ³n,Etiquetas"
        )

        for tarea in tareas:
            etiquetas_str = "|".join(tarea.etiquetas) if tarea.etiquetas else ""
            linea = f'{tarea.tarea_id},"{tarea.titulo}","{tarea.descripcion}",{tarea.prioridad},{tarea.estado},{tarea.asignado_a or ""},{tarea.fecha_creacion},{etiquetas_str}'
            lineas.append(linea)

        return "\n".join(lineas)

    @staticmethod
    def exportar_a_markdown(proyecto: Proyecto) -> str:
        """Exporta proyecto a formato Markdown"""
        lineas = []
        lineas.append(f"# {proyecto.nombre}\n")
        lineas.append(f"**DescripciÃ³n:** {proyecto.descripcion}\n")
        lineas.append(f"**Creado:** {proyecto.fecha_creacion}\n")
        lineas.append(f"**Total de tareas:** {proyecto.contar_tareas()}\n")

        for columna in proyecto.listar_columnas():
            lineas.append(f"## {columna.nombre}\n")

            if not columna.tareas:
                lineas.append("*(vacÃ­o)*\n")
            else:
                for tarea in columna.tareas:
                    lineas.append(
                        f"- **{tarea.titulo}** ({tarea.prioridad}, {tarea.estado})"
                    )
                    if tarea.descripcion:
                        lineas.append(f"  - {tarea.descripcion}")
                    if tarea.asignado_a:
                        lineas.append(f"  - Asignado a: {tarea.asignado_a}")
                    lineas.append("")

        return "\n".join(lineas)
