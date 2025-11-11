from models import  Tarea, Proyecto
from cli import CliInterface

#-----------------------------------------------------------------------------------
# CP401 Cambiar la prioridad de la tarea
def test_actualizar_prioridad_de_tarea():
    # Crear una tarea inicial con prioridad baja
    tarea = Tarea("Tarea de prueba", prioridad="Baja")

    # Guardar la fecha anterior (de creación)
    fecha_anterior = tarea.fecha_modificacion

    # Ejecutar la actualización
    tarea.actualizar(prioridad="Alta")

    # Verificar que cambió la prioridad correctamente
    assert tarea.prioridad == "Alta", "La prioridad no se actualizó correctamente"

    # Verificar que la fecha de modificación fue actualizada
    assert tarea.fecha_modificacion is not None, "No se actualizó la fecha de modificación"
    assert tarea.fecha_modificacion != fecha_anterior, "La fecha no cambió tras actualizar"

    # Verificar que no se pueden cambiar atributos no permitidos
    tarea.actualizar(no_valido="valor")
    assert not hasattr(tarea, "no_valido"), "Se agregó un atributo no permitido"

#---------------------------------------------------------------------------------------
# CP402 - Cambiar el estado de la tarea

def test_cambiar_estado_de_tarea():
    # Crear una tarea con estado inicial por defecto ("Pendiente")
    tarea = Tarea("Tarea de prueba")
    estado_anterior = tarea.estado
    fecha_anterior = tarea.fecha_modificacion

    # Actualizar el estado a "Completada"
    tarea.actualizar(estado="Completada")

    # Verificar que el estado haya cambiado
    assert tarea.estado == "Completada", "El estado no se actualizó correctamente"
    assert tarea.estado != estado_anterior, "El estado sigue siendo el mismo"

    # Verificar que la fecha de modificación cambió
    assert tarea.fecha_modificacion != fecha_anterior, "La fecha no cambió tras actualizar"

    # Verificar que no se pueden agregar atributos inválidos
    tarea.actualizar(invalido="valor")
    assert not hasattr(tarea, "invalido"), "Se agregó un atributo no permitido"


#--------------------------------------------------------------------------------------------------------------
# CP404 - Ver todos los detalles completos de la tarea

def test_ver_detalles_completos_tarea(monkeypatch, capsys):

    # Preparación del entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto Test CLI")
    columna = proyecto.agregar_columna("Pendiente")

    tarea = Tarea(
        "Tarea Detalle",
        descripcion="Descripción de prueba",
        prioridad="Alta",
        asignado_a="Carlos"
    )
    tarea.etiquetas = ["Importante", "Urgente"]
    columna.agregar_tarea(tarea)
    cli.proyecto_actual = proyecto

    # Simular interacción del usuario
    # "8" -> Ver detalles, "0" -> Guardar y volver
    inputs = iter(["8", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar la función
    cli.editar_tarea(columna, tarea)

    #Capturar la salida impresa
    salida = capsys.readouterr().out

    # Verificar los detalles mostrados
    assert "Tarea Detalle" in salida
    assert "Descripción de prueba" in salida
    assert "Alta" in salida
    assert "Carlos" in salida
    assert "Importante" in salida or "Urgente" in salida


#--------------------------------------------------------------------------------------------------
# CP501 - Buscar parcialmente el titulo 

def test_buscar_tarea_cli(monkeypatch, capsys):

    cli = CliInterface()
    proyecto = Proyecto("Proyecto Busqueda")
    col = proyecto.agregar_columna("Pendiente")

    tarea1 = Tarea("Redactar informe")
    tarea2 = Tarea("Revisar borrador")
    col.agregar_tarea(tarea1)
    col.agregar_tarea(tarea2)
    cli.proyecto_actual = proyecto

    # Simular los tres inputs del flujo completo
    inputs = iter(["redactar", "0", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cli.buscar_tarea()

    salida = capsys.readouterr().out

    assert "Redactar informe" in salida, "No se muestra la tarea buscada."
    assert "Revisar borrador" not in salida, "Se muestran tareas incorrectas."
    assert "RESULTADOS DE BUSQUEDA" in salida, "No se muestra el encabezado."

   
#--------------------------------------------------------------------------------------------------
# CP502 Mensaje cuando no hay resultados de búsqueda
def test_busqueda_sin_resultados(monkeypatch, capsys):

    # Crear el entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto sin coincidencias")
    col = proyecto.agregar_columna("Pendiente")

    # Agregar tareas que NO coincidan con el término
    col.agregar_tarea(Tarea("Diseñar portada"))
    col.agregar_tarea(Tarea("Planificar evento"))
    cli.proyecto_actual = proyecto

    # Simular entradas del usuario
    # "revisión" no existe → sin resultados
    # "" → presiona Enter para continuar
    inputs = iter(["revisión", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar el método real
    cli.buscar_tarea()

    # Capturar lo que se imprimió
    salida = capsys.readouterr().out

    # Verificar el mensaje esperado
    assert "No se encontraron tareas" in salida, "No muestra el mensaje de búsqueda vacía."


#--------------------------------------------------------------------------------------------------
# CP601 - muestran todas las columnas del proyecto actúal
def test_listar_columnas_proyecto():
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

#----------------------------------------------------------------------------------------------------
# CP602 - Se muestran todas las tareas dentro de cada columna
def test_listar_tareas_columna(monkeypatch, capsys):

    # Preparar entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto con Tareas")

    # Crear columnas
    col_pendiente = proyecto.agregar_columna("Pendiente")
    col_en_progreso = proyecto.agregar_columna("En Progreso")

    # Crear tareas y agregarlas a las columnas
    tarea1 = Tarea("Redactar informe", prioridad="Alta")
    tarea2 = Tarea("Diseñar logo", prioridad="Media")
    col_pendiente.agregar_tarea(tarea1)
    col_en_progreso.agregar_tarea(tarea2)

    cli.proyecto_actual = proyecto

    # Simular presionar Enter al final
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar método
    cli.ver_tablero()

    # Capturar salida impresa
    salida = capsys.readouterr().out

    # Verificar que las tareas aparezcan en la salida
    assert "Redactar informe" in salida, "No se muestra la tarea 'Redactar informe'."
    assert "Diseñar logo" in salida, "No se muestra la tarea 'Diseñar logo'."
    assert "+- Pendiente" in salida, "No se muestra la columna 'Pendiente'."
    assert "+- En Progreso" in salida, "No se muestra la columna 'En Progreso'."
    

#----------------------------------------------------------------------------------------------------
#CP603 - Se muestra el título de cada tarea en el tablero
def test_mostrar_titulo_tareas_en_tablero(monkeypatch, capsys):
    
    # Preparar entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto Títulos")
    col = proyecto.agregar_columna("Pendiente")

    # Crear tareas
    tarea1 = Tarea("Revisar código")

    # Agregar tareas a la columna
    col.agregar_tarea(tarea1)
    cli.proyecto_actual = proyecto

    # Simular presionar Enter
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # jecutar método
    cli.ver_tablero()

    # Capturar salida
    salida = capsys.readouterr().out

    # Verificar títulos
    assert "Revisar código" in salida, "No se muestra el título 'Revisar código'."
 

#--------------------------------------------------------------------------------------------------
# CP604 - Mostrar el ID de la tarea 
def test_mostrar_id_tareas_en_tablero(monkeypatch, capsys):
    

    # Preparar entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto IDs")
    col = proyecto.agregar_columna("Pendiente")

    # Crear tarea
    tarea1 = Tarea("Revisar código")

    # Agregar tarea a la columna
    col.agregar_tarea(tarea1)
    cli.proyecto_actual = proyecto

    # Simular presionar Enter
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar método
    cli.ver_tablero()

    # Capturar salida
    salida = capsys.readouterr().out

    # Verificar ID (primeros 8 caracteres)
    assert tarea1.tarea_id[:8] in salida, f"❌ No se muestra el ID de la tarea '{tarea1.titulo}'."

#--------------------------------------------------------------------------------------------------
# CP605 - Guardar y cargar usuarios
def test_mostrar_usuario_asignado_o_sin_asignar(monkeypatch, capsys):
    

    # Preparar entorno
    cli = CliInterface()
    proyecto = Proyecto("Proyecto Usuarios")
    col = proyecto.agregar_columna("Pendiente")

    # Crear tareas
    tarea1 = Tarea("Revisar código", asignado_a="Daniel")
    tarea2 = Tarea("Documentar API")  # Sin asignar

    # Agregar tareas a la columna
    col.agregar_tarea(tarea1)
    col.agregar_tarea(tarea2)
    cli.proyecto_actual = proyecto

    # Simular presionar Enter (porque ver_tablero usa input())
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar método
    cli.ver_tablero()

    # Capturar salida
    salida = capsys.readouterr().out

    # Verificar usuario asignado o "Sin asignar"
    assert "Asignado: Daniel" in salida, "No se muestra el usuario asignado 'Daniel'."
    assert "Asignado: Sin asignar" in salida, "No se muestra 'Sin asignar' para tareas sin usuario."



  



