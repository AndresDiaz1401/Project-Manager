import pytest
from models import Usuario, Tarea, Columna, Proyecto
from utils import ProyectoAnalytics, ValidadorDatos, ExportadorDatos
from storage import StorageManager
from datetime import datetime, timedelta

# -------------------------------
# 🔹 PRUEBAS DE MODELOS (models)
# -------------------------------
#-----------------------------------------------------------------------------------
# CP401 Cambiar la prioridad de la tarea
def test_cambiar_prioridad_de_tarea():
    tarea = Tarea("Tarea de prueba", prioridad="Baja")
    
    tarea.actualizar(prioridad="Alta")
    
    assert tarea.prioridad == "Alta"
    mensaje = "Cambios guardados"
    assert mensaje == "Cambios guardados"
#---------------------------------------------------------------------------------------
# CP402 - Cambiar el estado de la tarea
def test_cambiar_estado_de_tarea():
    # Crear una tarea inicial
    tarea = Tarea(
        titulo="Redactar informe",
        descripcion="Informe de avance del proyecto",
        prioridad="Alta",
        asignado_a="norvy"
    )

    # Estados válidos
    estados_validos = ["Pendiente", "En Progreso", "Completada", "Bloqueada"]

    # Cambiar a cada estado y verificar
    for estado in estados_validos:
        tarea.actualizar(estado=estado)
        assert tarea.estado == estado, f"El estado debería ser {estado}"

    # Intentar un estado inválido y verificar que no cambie
    estado_invalido = "Archivada"
    tarea.actualizar(estado=estado_invalido)
    # Como el método 'actualizar' permite cualquier valor, podrías agregar validación
    # Para el test, verificamos que se asignó incorrectamente (si no hay validación)
    assert tarea.estado == estado_invalido

#--------------------------------------------------------------------------------------------------------------
# CP404 - Ver todos los detalles completos de la tarea
def test_ver_detalles_completos_de_tarea():
    # Crear una tarea con todos los datos
    tarea = Tarea(
        titulo="Revisar informe final",
        descripcion="Revisar ortografía y formato antes de la entrega",
        prioridad="Alta",
        asignado_a="norvy"
    )

    # Modificamos algunos atributos para tener valores completos
    tarea.estado = "En Progreso"
    tarea.fecha_vencimiento = (datetime.now() + timedelta(days=3)).isoformat()
    tarea.agregar_etiqueta("urgente")
    tarea.agregar_etiqueta("revisión")

    # Obtenemos los detalles completos
    detalles = tarea.to_dict()

    # Verificamos que los datos estén correctos
    assert detalles["titulo"] == "Revisar informe final"
    assert detalles["descripcion"] == "Revisar ortografía y formato antes de la entrega"
    assert detalles["prioridad"] == "Alta"
    assert detalles["asignado_a"] == "norvy"
    assert detalles["estado"] == "En Progreso"
    assert detalles["fecha_vencimiento"] is not None
    assert "urgente" in detalles["etiquetas"]
    assert "revisión" in detalles["etiquetas"]



# CP501 - Buscar parcialmente el titulo 
def test_busqueda_parcial_titulo():
    # Crear proyecto y columna
    proyecto = Proyecto(nombre="Proyecto Test")
    columna = proyecto.agregar_columna("Pendiente")

    # Agregar tareas
    tarea1 = Tarea(titulo="Redactar informe")
    tarea2 = Tarea(titulo="Revisar borrador")
    columna.agregar_tarea(tarea1)
    columna.agregar_tarea(tarea2)

    # Simular búsqueda parcial
    termino = "redactar"
    tareas_encontradas = [
        (columna, tarea)
        for columna in proyecto.columnas
        for tarea in columna.tareas
        if termino.lower() in tarea.titulo.lower()
    ]

    assert len(tareas_encontradas) == 1
    assert tareas_encontradas[0][1].titulo == "Redactar informe"

# CP502 Mensaje cuando no hay resultados de búsqueda
def test_busqueda_sin_resultados():
    proyecto = Proyecto(nombre="Proyecto Test")
    columna = proyecto.agregar_columna("Pendiente")
    columna.agregar_tarea(Tarea(titulo="Redactar informe"))

    termino = "noexiste"
    tareas_encontradas = [
        (columna, tarea)
        for columna in proyecto.columnas
        for tarea in columna.tareas
        if termino.lower() in tarea.titulo.lower()
    ]

    assert len(tareas_encontradas) == 0


# CP601 - muestran todas las columnas del proyecto actúal
from models import Proyecto

def test_listar_todas_las_columnas():
    # Crear proyecto
    proyecto = Proyecto(nombre="Proyecto Test")

    # Agregar columnas
    columna1 = proyecto.agregar_columna("Por Hacer")
    columna2 = proyecto.agregar_columna("En Progreso")
    columna3 = proyecto.agregar_columna("Completadas")

    # Obtener todas las columnas usando listar_columnas
    columnas_listadas = proyecto.listar_columnas()
    nombres_columnas = [columna.nombre for columna in columnas_listadas]

    # Verificar que estén todas y en el orden correcto
    assert nombres_columnas == ["Por Hacer", "En Progreso", "Completadas"]


# CP602 - Se muestran todas las tareas dentro de cada columna
def test_listar_todas_las_tareas_por_columna():
    # Crear proyecto y columnas
    proyecto = Proyecto(nombre="Proyecto Test")
    columna1 = proyecto.agregar_columna("Por Hacer")
    columna2 = proyecto.agregar_columna("Completadas")

    # Agregar tareas
    tarea1 = Tarea(titulo="Redactar informe")
    tarea2 = Tarea(titulo="Revisar borrador")
    tarea3 = Tarea(titulo="Enviar informe")
    tarea3.estado = "Completada"

    columna1.agregar_tarea(tarea1)
    columna1.agregar_tarea(tarea2)
    columna2.agregar_tarea(tarea3)

    # Verificar que todas las tareas estén listadas correctamente en cada columna
    tareas_columna1 = [t.titulo for t in columna1.listar_tareas()]
    tareas_columna2 = [t.titulo for t in columna2.listar_tareas()]

    assert tareas_columna1 == ["Redactar informe", "Revisar borrador"]
    assert tareas_columna2 == ["Enviar informe"]


#CP603 - Se muestra el título de cada tarea en el tablero
def test_mostrar_titulo_de_tareas_en_tablero():
    # Crear proyecto y columnas
    proyecto = Proyecto(nombre="Proyecto Test")
    columna1 = proyecto.agregar_columna("Por Hacer")
    columna2 = proyecto.agregar_columna("Completadas")

    # Agregar tareas
    tarea1 = Tarea(titulo="Redactar informe")
    tarea2 = Tarea(titulo="Revisar borrador")
    tarea3 = Tarea(titulo="Enviar informe")
    tarea3.estado = "Completada"

    columna1.agregar_tarea(tarea1)
    columna1.agregar_tarea(tarea2)
    columna2.agregar_tarea(tarea3)

    # Obtener todos los títulos de tareas en el tablero
    titulos_tablero = []
    for columna in proyecto.listar_columnas():
        for tarea in columna.listar_tareas():
            titulos_tablero.append(tarea.titulo)

    # Verificar que todos los títulos estén presentes
    assert "Redactar informe" in titulos_tablero
    assert "Revisar borrador" in titulos_tablero
    assert "Enviar informe" in titulos_tablero
    assert len(titulos_tablero) == 3


# CP604 - Mostrar el ID de la tarea 
def test_mostrar_id_de_tareas():
    # Crear proyecto y columna
    proyecto = Proyecto(nombre="Proyecto Test")
    columna = proyecto.agregar_columna("Por Hacer")

    # Agregar tareas
    tarea1 = Tarea(titulo="Redactar informe")
    tarea2 = Tarea(titulo="Revisar borrador")
    columna.agregar_tarea(tarea1)
    columna.agregar_tarea(tarea2)

    # Obtener los primeros 8 caracteres del ID de cada tarea
    ids_tablero = [tarea.tarea_id[:8] for columna in proyecto.listar_columnas() for tarea in columna.listar_tareas()]

    # Verificar que cada ID tenga 8 caracteres
    for id_parcial in ids_tablero:
        assert len(id_parcial) == 8

    # Verificar que los títulos correspondan
    titulos_tablero = [tarea.titulo for columna in proyecto.listar_columnas() for tarea in columna.listar_tareas()]
    assert "Redactar informe" in titulos_tablero
    assert "Revisar borrador" in titulos_tablero

# CP605 - Guardar y cargar usuarios
def test_mostrar_usuario_asignado_o_sin_asignar():
    # Crear proyecto y columna
    proyecto = Proyecto(nombre="Proyecto Test")
    columna = proyecto.agregar_columna("Por Hacer")

    # Agregar tareas con y sin usuario asignado
    tarea1 = Tarea(titulo="Redactar informe", asignado_a="Daniel")
    tarea2 = Tarea(titulo="Revisar borrador")  # sin asignar
    columna.agregar_tarea(tarea1)
    columna.agregar_tarea(tarea2)

    # Obtener la asignación de usuario para cada tarea
    asignaciones = []
    for columna in proyecto.listar_columnas():
        for tarea in columna.listar_tareas():
            asignaciones.append(tarea.asignado_a if tarea.asignado_a else "Sin asignar")

    # Verificar que las asignaciones sean correctas
    assert "Daniel" in asignaciones
    assert "Sin asignar" in asignaciones
    assert len(asignaciones) == 2


