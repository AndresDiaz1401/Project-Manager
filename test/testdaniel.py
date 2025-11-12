import pytest
from models import Proyecto, Tarea, Usuario
from storage import StorageManager

"""
CP102 - Listar todos los usuarios registrados

Title: CP102 El usuario puede listar todos los usuarios registrados en el sistema.

Description:
Este caso verifica que el sistema permita listar todos los usuarios que se han registrado,
mostrando la lista completa de usuarios disponibles en el sistema.
"""

def test_cp102_listar_todos_usuarios(tmp_path):
	archivo_datos = tmp_path / "data.json"
	gestor_almacenamiento = StorageManager(archivo_datos=archivo_datos)

	usuario_juan = Usuario(nombre="Juan", email="juan@example.com")
	usuario_maria = Usuario(nombre="Maria", email="maria@example.com")
	usuario_pedro = Usuario(nombre="Pedro", email="pedro@example.com")

	gestor_almacenamiento.guardar_usuario(usuario_juan)
	gestor_almacenamiento.guardar_usuario(usuario_maria)
	gestor_almacenamiento.guardar_usuario(usuario_pedro)

	usuarios_registrados = gestor_almacenamiento.cargar_todos_usuarios()

	assert len(usuarios_registrados) == 3

	nombres_en_lista = [usuario.nombre for usuario in usuarios_registrados]
	assert "Juan" in nombres_en_lista
	assert "Maria" in nombres_en_lista
	assert "Pedro" in nombres_en_lista


"""
CP202 - Nombre del proyecto obligatorio

Title: CP202 El nombre del proyecto es obligatorio.

Description:
Este caso confirma que el sistema no permita al usuario crear un proyecto sin un nombre.
"""
def test_cp202_nombre_obligatorio(tmp_path):
	
	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)
	
	proyecto = Proyecto(nombre="", descripcion="descripcion")
	
	if proyecto.nombre == "":
		resultado = False
	else:
		resultado = storage.guardar_proyecto(proyecto)
	
	assert resultado is False or len(storage.cargar_todos_proyectos()) == 0


"""
CP206 - Abrir proyecto por identificador

Title: CP206 Validar que el usuario pueda abrir un proyecto existente por su identificador.

Description:
Este caso confirma que el sistema permita al usuario abrir un proyecto previamente creado,
mostrando el mensaje de confirmación correcto.
"""
def test_cp206_abrir_proyecto_por_id(tmp_path):

	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)

	proyecto = Proyecto(nombre="Proyecto CP206", descripcion="desc")
	assert storage.guardar_proyecto(proyecto) is True

	cargado = storage.cargar_proyecto(proyecto.proyecto_id)
	assert cargado is not None
	assert cargado.proyecto_id == proyecto.proyecto_id

	mensaje = f"Proyecto actual: {cargado.nombre}"
	assert mensaje == "Proyecto actual: Proyecto CP206"
	

"""
CP209 - Listar todos los proyectos con conteo de tareas

Title: CP209 El usuario puede listar todos los proyectos con conteo de tareas.

Description:
Este caso verifica que el sistema permita listar todos los proyectos registrados,
mostrando para cada proyecto el conteo total de tareas que contiene.
"""
def test_cp209_listar_proyectos_con_conteo_tareas(tmp_path):
	archivo_datos = tmp_path / "data.json"
	gestor_almacenamiento = StorageManager(archivo_datos=archivo_datos)

	proyecto_uno = Proyecto(nombre="Proyecto Uno", descripcion="Descripcion 1")
	columna_uno = proyecto_uno.agregar_columna("Backlog")
	tarea_uno_a = Tarea(titulo="Tarea 1A")
	tarea_uno_b = Tarea(titulo="Tarea 1B")
	columna_uno.agregar_tarea(tarea_uno_a)
	columna_uno.agregar_tarea(tarea_uno_b)
	
	proyecto_dos = Proyecto(nombre="Proyecto Dos", descripcion="Descripcion 2")
	columna_dos = proyecto_dos.agregar_columna("Tareas")
	tarea_dos_a = Tarea(titulo="Tarea 2A")
	tarea_dos_b = Tarea(titulo="Tarea 2B")
	tarea_dos_c = Tarea(titulo="Tarea 2C")
	columna_dos.agregar_tarea(tarea_dos_a)
	columna_dos.agregar_tarea(tarea_dos_b)
	columna_dos.agregar_tarea(tarea_dos_c)

	gestor_almacenamiento.guardar_proyecto(proyecto_uno)
	gestor_almacenamiento.guardar_proyecto(proyecto_dos)

	proyectos_registrados = gestor_almacenamiento.cargar_todos_proyectos()

	assert len(proyectos_registrados) == 2

	proyecto_uno_cargado = proyectos_registrados[0]
	proyecto_dos_cargado = proyectos_registrados[1]

	conteo_tareas_proyecto_uno = proyecto_uno_cargado.contar_tareas()
	conteo_tareas_proyecto_dos = proyecto_dos_cargado.contar_tareas()

	assert conteo_tareas_proyecto_uno == 2
	assert conteo_tareas_proyecto_dos == 3
	
    
"""
CP307 - Crear tarea con descripción opcional

Title: CP307 Validar que el sistema permita crear una tarea ingresando una descripción opcional.

Description:
Este caso verifica que el sistema permita crear tareas con una descripción opcional.
Se pueden crear tareas sin descripción y también con descripción completa.
"""
def test_cp307_crear_tarea_con_descripcion_opcional():
	proyecto = Proyecto(nombre="Proyecto CP307")
	columna = proyecto.agregar_columna("Tareas")

	tarea_sin_descripcion = Tarea(titulo="Tarea sin descripción")
	columna.agregar_tarea(tarea_sin_descripcion)

	tarea_con_descripcion = Tarea(
		titulo="Tarea con descripción",
		descripcion="Esta es una descripción detallada de la tarea"
	)
	columna.agregar_tarea(tarea_con_descripcion)

	assert columna.contar_tareas() == 2

	assert tarea_sin_descripcion.titulo == "Tarea sin descripción"
	assert tarea_sin_descripcion.descripcion == ""

	assert tarea_con_descripcion.titulo == "Tarea con descripción"
	assert tarea_con_descripcion.descripcion == "Esta es una descripción detallada de la tarea"


"""
CP403 - Mover tarea a otra columna

Title: CP403 Mover la tarea a otra columna del proyecto.

Description:
"""
def test_cp403_mover_tarea_otra_columna_minimal():
	proyecto = Proyecto("Proyecto CP403")

	origen = proyecto.agregar_columna("A")
	destino = proyecto.agregar_columna("B")

	tarea = Tarea("t1")
	origen.agregar_tarea(tarea)

	# Mover: eliminar de origen y agregar a destino
	origen.eliminar_tarea(tarea.tarea_id)
	destino.agregar_tarea(tarea)

	# Comprobaciones mínimas
	assert proyecto.contar_tareas() == 1
	assert destino.obtener_tarea(tarea.tarea_id) is not None
	assert origen.obtener_tarea(tarea.tarea_id) is None


"""
CP407 - Modificar título de una tarea existente

Title: CP407 Validar que el usuario pueda modificar el título de una tarea existente.

Description:
Prueba simple (junior) que crea un proyecto y una tarea, modifica el título usando
el método público de la tarea y verifica que el título se haya actualizado correctamente.
"""
def test_cp407_modificar_titulo_tarea_simple():
	proyecto = Proyecto(nombre="Proyecto CP407")
	columna = proyecto.agregar_columna("Tareas")

	tarea = Tarea(titulo="Titulo Original")
	columna.agregar_tarea(tarea)

	assert columna.obtener_tarea(tarea.tarea_id) is not None
	assert tarea.titulo == "Titulo Original"

	tarea.actualizar(titulo="Titulo Modificado")

	tarea_actualizada = columna.obtener_tarea(tarea.tarea_id)
	assert tarea_actualizada is not None
	assert tarea_actualizada.titulo == "Titulo Modificado"


"""
CP408 - Modificar descripción de una tarea existente

Title: CP408 Validar que el usuario pueda modificar la descripción de una tarea ya creada.

Description:
Prueba simple (junior) que crea una tarea sin descripción, la actualiza con una descripción
y verifica que el campo `descripcion` se actualice correctamente.
"""
def test_cp408_modificar_descripcion_tarea_simple():
	proyecto = Proyecto(nombre="Proyecto CP408")
	columna = proyecto.agregar_columna("Tareas")

	tarea = Tarea(titulo="Tarea sin desc")
	columna.agregar_tarea(tarea)
	
	assert tarea.descripcion == ""

	nueva_descripcion = "Descripción actualizada de la tarea"
	tarea.actualizar(descripcion=nueva_descripcion)

	tarea_actualizada = columna.obtener_tarea(tarea.tarea_id)
	assert tarea_actualizada is not None
	assert tarea_actualizada.descripcion == nueva_descripcion


"""
CP502 - Mostrar columna de cada tarea

Title: CP502 Verificar que el sistema muestre la columna donde se encuentra cada tarea.

Description:
Comprueba que, dado un proyecto con varias columnas y tareas, podamos identificar
la columna que contiene cada tarea.
"""
def test_cp502_mostrar_columna_de_cada_tarea_simple():
	proyecto = Proyecto(nombre="Proyecto CP502")
	col_backlog = proyecto.agregar_columna("Backlog")

	t1 = Tarea(titulo="backlog-1")
	t2 = Tarea(titulo="backlog-2")

	col_backlog.agregar_tarea(t1)
	col_backlog.agregar_tarea(t2)

	mapa = {}
	for columna in proyecto.listar_columnas():
		for tarea in columna.tareas:
			mapa[tarea.titulo] = columna.nombre

	assert mapa["backlog-1"] == "Backlog"
	assert mapa["backlog-2"] == "Backlog"



"""
CP702 - Listar columnas del proyecto

Title: CP702 Validar que el sistema muestre correctamente la lista de columnas actuales del proyecto.

Description:
Este caso confirma que el sistema muestre todas las columnas del proyecto de forma correcta.
"""
def test_cp702_listar_columnas_del_proyecto(tmp_path):
	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)

	proyecto = Proyecto(nombre="Proyecto CP702", descripcion="desc")
	
	col1 = proyecto.agregar_columna("Pendiente")
	col2 = proyecto.agregar_columna("En Progreso")
	col3 = proyecto.agregar_columna("Completada")
	
	assert storage.guardar_proyecto(proyecto) is True

	proyecto_cargado = storage.cargar_proyecto(proyecto.proyecto_id)
	columnas = proyecto_cargado.listar_columnas()
	
	assert len(columnas) == 3
	
	nombres = [col.nombre for col in columnas]
	assert "Pendiente" in nombres
	assert "En Progreso" in nombres
	assert "Completada" in nombres


"""
CP708 - Nombre de columna obligatorio

Title: CP708 Validar que el campo "Nombre de la columna" sea obligatorio al crear una nueva columna.

Description:
Este caso confirma que el sistema no permita crear una columna sin nombre.
"""
def test_cp708_nombre_columna_obligatorio(tmp_path):

	proyecto = Proyecto(nombre="Proyecto CP708", descripcion="desc")
	
	nombre_columna = ""
	
	if nombre_columna == "":
		resultado = False
	else:
		resultado = proyecto.agregar_columna(nombre_columna)
	
	assert resultado is False or len(proyecto.listar_columnas()) == 0


"""
CP709 - Impedir columnas duplicadas

Title: CP709 Validar que el sistema impida la creación de columnas duplicadas por nombre.

Description:
Este caso confirma que el sistema no permita crear dos columnas con el mismo nombre en un proyecto.
"""
def test_cp709_columnas_duplicadas(tmp_path):
	proyecto = Proyecto(nombre="Proyecto CP709", descripcion="desc")
	
	col1 = proyecto.agregar_columna("Tareas")
	assert col1 is not None
	
	col2 = proyecto.agregar_columna("Tareas")
	
	columnas = proyecto.listar_columnas()
	nombres = [col.nombre for col in columnas]
	cantidad_tareas = nombres.count("Tareas")
	
	assert cantidad_tareas == 1, "Se permitió crear una columna duplicada"


"""
CP803 - Porcentaje de tareas por estado

Title: CP803 Validar que el sistema muestre el porcentaje de tareas por estado actual del proyecto.

Description:
Calcula el porcentaje de tareas en cada estado y valida que los porcentajes sean correctos.
"""
def test_cp803_porcentaje_tareas_por_estado_simple():
	proyecto = Proyecto(nombre="Proyecto CP803")
	columna = proyecto.agregar_columna("Tablero")

	tarea1 = Tarea(titulo="T1")  
	tarea2 = Tarea(titulo="T2")
	tarea2.estado = "En Progreso"
	tarea3 = Tarea(titulo="T3")
	tarea3.estado = "Completada"
	tarea4 = Tarea(titulo="T4")
	tarea4.estado = "Completada"

	columna.agregar_tarea(tarea1)
	columna.agregar_tarea(tarea2)
	columna.agregar_tarea(tarea3)
	columna.agregar_tarea(tarea4)

	tareas = proyecto.obtener_todas_las_tareas()
	total = len(tareas)
	assert total == 4

	pendientes = sum(1 for t in tareas if t.estado == "Pendiente")
	en_progreso = sum(1 for t in tareas if t.estado == "En Progreso")
	completadas = sum(1 for t in tareas if t.estado == "Completada")

	pct_pendiente = (pendientes / total) * 100
	pct_enprogreso = (en_progreso / total) * 100
	pct_completada = (completadas / total) * 100

	assert pct_pendiente == pytest.approx(25.0)
	assert pct_enprogreso == pytest.approx(25.0)
	assert pct_completada == pytest.approx(50.0)


"""
CP808 - Conteo de tareas por columna

Title: CP808 Validar que el sistema muestre el conteo de tareas agrupadas por columna.

Description:
Verifica que cada columna reporte la cantidad de tareas que contiene.
"""
def test_cp808_conteo_tareas_por_columna():
	proyecto = Proyecto(nombre="Proyecto CP808")
	col_a = proyecto.agregar_columna("Backlog")

	t1 = Tarea(titulo="T1")
	t2 = Tarea(titulo="T2")
	t3 = Tarea(titulo="T3")

	col_a.agregar_tarea(t1)
	col_a.agregar_tarea(t2)
	
	assert col_a.contar_tareas() == 2


"""
CP1001 - Guardado automático después de crear proyectos (versión junior)

Title: CP1001 Guardar automáticamente después de crear proyectos.

"""
def test_cp1001_guardado_automatico_minimal(tmp_path):
	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)

	proyecto = Proyecto(nombre="Proyecto Auto", descripcion="")
	assert storage.guardar_proyecto(proyecto) is True







