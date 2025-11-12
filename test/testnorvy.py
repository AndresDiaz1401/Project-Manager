from models import  Tarea, Proyecto, Usuario
from cli import CliInterface
from utils import ExportadorDatos

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
    assert tarea1.tarea_id[:8] in salida, f"No se muestra el ID de la tarea '{tarea1.titulo}'."

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

    # Simular presionar Enter 
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar método
    cli.ver_tablero()

    # Capturar salida
    salida = capsys.readouterr().out

    # Verificar usuario asignado o Sin asignar
    assert "Asignado: Daniel" in salida, "No se muestra el usuario asignado 'Daniel'."
    assert "Asignado: Sin asignar" in salida, "No se muestra 'Sin asignar' para tareas sin usuario."

#----------------------------------------------------------------------------------------------------
# CP106 - seleccionar un usuario existente como usuario actual
def test_seleccionar_usuario_existente_como_actual(monkeypatch, capsys):
   
    cli = CliInterface()

    # Crear usuarios directamente con los métodos del sistema
    usuario1 = Usuario(nombre="Ana", email="ana@example.com")
    usuario2 = Usuario(nombre="Luis", email="luis@example.com")

    cli.storage.guardar_usuario(usuario1)
    cli.storage.guardar_usuario(usuario2)

    # Simular entradas del usuario
    inputs = iter(["2", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar el método real
    cli.seleccionar_usuario()

    # Capturar salida
    salida = capsys.readouterr().out

    # Verificar resultados
    assert cli.usuario_actual is not None, "No se estableció ningún usuario actual."
    assert cli.usuario_actual.nombre == "Luis", "No se seleccionó el usuario correcto."
    assert "Luis" in salida, " No se muestra el nombre del usuario seleccionado en la interfaz."


#----------------------------------------------------------------------------------
# CP206 - Crear automáticamente tres columnas: Pendiente, En Progreso, Completada
def test_creacion_proyecto_con_columnas_automaticas(monkeypatch):
   

    cli = CliInterface()

    # Simular las entradas del usuario:4
    inputs = iter(["Proyecto Prueba", "", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar el método
    cli.crear_proyecto()

    # Recuperar el proyecto recién creado
    proyectos = cli.storage.cargar_todos_proyectos()
    proyecto = next((p for p in proyectos if p.nombre == "Proyecto Prueba"), None)

    # Validaciones
    assert proyecto is not None, "No se creó el proyecto correctamente."
    nombres_columnas = [c.nombre for c in proyecto.columnas]
    assert nombres_columnas == ["Pendiente", "En Progreso", "Completada"], \
        f"Columnas creadas incorrectas: {nombres_columnas}"

    
#----------------------------------------------------------------------------------
# CP306 - Se registran automáticamente fechas de creación y modificación
def test_fechas_creacion_y_modificacion():

    tarea = Tarea("Tarea con fechas")

    # Verificar que ambas fechas existan
    assert tarea.fecha_creacion is not None, "No se registró fecha de creación."
    assert tarea.fecha_modificacion is not None, "No se registró fecha de modificación."

#-------------------------------------------------------------------------------------------
#CP406 Verificar actualización automática de la fecha de modificación
def test_actualiza_fecha_modificacion_despues_de_cambio():
    
    tarea = Tarea("Revisar informe")
    fecha_inicial = tarea.fecha_modificacion

    # Modificar algún atributo de la tarea
    tarea.actualizar(descripcion="Nueva descripción agregada")

    # Verificar que la fecha haya cambiado
    assert tarea.fecha_modificacion != fecha_inicial, " La fecha de modificación no se actualizó."
#--------------------------------------------------------------------------------------
#CP902 Exportación a CSV incluye las columnas requeridas    
def test_exportar_csv_campos_basicos():
    # Crear proyecto
    proyecto = Proyecto("Proyecto Test")

    # Crear columna y agregar al proyecto
    columna = proyecto.agregar_columna("Pendiente")

    # Crear tarea de prueba
    tarea = Tarea(
        titulo="Tarea 1",
        descripcion="Descripción de prueba",
        prioridad="Alta",
        asignado_a="Usuario Test"
    )
    
    # Agregar tarea a la columna
    columna.agregar_tarea(tarea)

    # Exportar a CSV
    csv_resultado = ExportadorDatos.exportar_a_csv(proyecto)

    # Validar encabezado
    encabezado_esperado = "ID Tarea,TÃ­tulo,DescripciÃ³n,Prioridad,Estado,Asignado A,Fecha CreaciÃ³n,Etiquetas"
    assert csv_resultado.split("\n")[0] == encabezado_esperado

    # Validar que la tarea está en CSV
    primera_linea = csv_resultado.split("\n")[1]
    assert "Tarea 1" in primera_linea
    assert "Descripción de prueba" in primera_linea
    assert "Alta" in primera_linea
    assert "Pendiente" in primera_linea
    assert "Usuario Test" in primera_linea


#---------------------------------------------------------------------------------------
#CP903 exportar el proyecto a formato JSON
def test_exportar_a_json_simple():
    proyecto = Proyecto("Proyecto prueba")
    
    resultado = ExportadorDatos.exportar_a_json_simple(proyecto)
    
    # Solo verificar que la función retorna un diccionario
    assert isinstance(resultado, dict)
#--------------------------------------------------------------------------------------
#CP803  total de tareas del proyecto
def test_mostrar_total_tareas(monkeypatch, capsys):
    # Crear la interfaz
    cli = CliInterface()

    # Crear un proyecto de prueba con una columna y tareas
    proyecto = Proyecto("Proyecto Test", "Descripcion Test", propietario_id="1")
    columna = proyecto.agregar_columna("Pendiente")

    # Agregar tareas
    tarea1 = Tarea("Tarea 1", "Desc 1", prioridad="Alta")
    tarea2 = Tarea("Tarea 2", "Desc 2", prioridad="Media")
    columna.agregar_tarea(tarea1)
    columna.agregar_tarea(tarea2)

    # Asignar proyecto actual
    cli.proyecto_actual = proyecto

    # Simular inputs del usuario
    inputs = iter(["5", "", "6"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar el menú de proyecto actual
    cli.mostrar_menu_proyecto_actual()

    # Capturar la salida
    salida = capsys.readouterr().out

    # Verificar que se muestra el total de tareas
    assert "Total de tareas: 2" in salida


#---------------------------------------------------------------------------------------
#CP804 conteo de tareas por nivel de prioridad
def test_ver_estadisticas(monkeypatch, capsys):
    # Crear la interfaz
    cli = CliInterface()
    
    # Crear un proyecto de prueba con una columna y tareas
    proyecto = Proyecto("Proyecto Test", "Descripcion Test", propietario_id="1")
    columna = proyecto.agregar_columna("Pendiente")
    
    # Agregar tareas
    tarea1 = Tarea("Tarea 1", "Desc 1", prioridad="Alta")
    tarea2 = Tarea("Tarea 2", "Desc 2", prioridad="Media")
    columna.agregar_tarea(tarea1)
    columna.agregar_tarea(tarea2)
    
    # Asignar proyecto actual
    cli.proyecto_actual = proyecto

    # Simular inputs del usuario
    inputs = iter(["5", "", "6"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


    # Llamar al menú de proyecto actual
    cli.mostrar_menu_proyecto_actual()
    
    # Capturar salida
    salida = capsys.readouterr().out
    
    # Verificar que se imprime el título de estadisticas y las tareas
    assert "ESTADISTICAS: Proyecto Test" in salida
    assert "Total de tareas: 2" in salida
    assert "POR ESTADO:" in salida
    assert "Pendiente: 2" in salida
    assert "POR PRIORIDAD:" in salida
    assert "Alta: 1" in salida
    assert "Media: 1" in salida









  



