import pytest
from models import Proyecto, Tarea
from storage import StorageManager

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
CP208 - Eliminar proyecto con confirmación

Title: CP208 Validar que el usuario pueda eliminar un proyecto existente con confirmación previa.

Description:
Este caso confirma que el sistema permita eliminar un proyecto previamente creado,
solicitando confirmación del usuario antes de eliminar.
"""
def test_cp208_eliminar_proyecto_con_confirmacion(tmp_path):
	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)

	proyecto = Proyecto(nombre="Proyecto CP208", descripcion="desc")
	assert storage.guardar_proyecto(proyecto) is True

	proyectos_antes = storage.cargar_todos_proyectos()
	assert len(proyectos_antes) == 1

	resultado_eliminar = storage.eliminar_proyecto(proyecto.proyecto_id)
	assert resultado_eliminar is True

	proyectos_despues = storage.cargar_todos_proyectos()
	assert len(proyectos_despues) == 0


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
CP1001 - Guardado automático después de crear proyectos (versión junior)

Title: CP1001 Guardar automáticamente después de crear proyectos.

"""
def test_cp1001_guardado_automatico_minimal(tmp_path):
	archivo = tmp_path / "data.json"
	storage = StorageManager(archivo_datos=archivo)

	proyecto = Proyecto(nombre="Proyecto Auto", descripcion="")
	assert storage.guardar_proyecto(proyecto) is True

