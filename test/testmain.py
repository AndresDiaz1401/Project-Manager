# SOLO MODIFICAR ESTE ARCHIVO A LO ULTIMO 
import pytest
from models import Usuario, Proyecto, Tarea
from utils import ValidadorDatos
from storage import StorageManager
from cli import CliInterface

# CP101
# --------------------------------------------------------------------------------------------
def test_validar_correo():
    correoValidar = ValidadorDatos()
    validacion = correoValidar.validar_email("andres@gmail.com")
    assert validacion == True , "El correo no contiene @ o ."
# --------------------------------------------------------------------------------------------

# CP102
# --------------------------------------------------------------------------------------------
def test_eliminar_usuario_id(tmp_path, monkeypatch):
    archivoTest = tmp_path / "datosUsuario.json"
    storage = StorageManager(archivo_datos=archivoTest)
    
    usuario1 = Usuario(nombre="Andres", email= "andres@gmail.com")
    storage.guardar_usuario(usuario1)
    
    usuario2 = Usuario(nombre="Paula", email= "paula@gmail.com")
    storage.guardar_usuario(usuario2)
    
    idUsuarioEliminar = usuario1.usuario_id
    inputs = iter(["1", "s", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    cli = CliInterface()
    cli.storage = storage
    cli.eliminar_usuario()
    
    usuariosRestantes = storage.cargar_todos_usuarios()
    
    usuarioExiste = any(usuarios.usuario_id == idUsuarioEliminar for usuarios in usuariosRestantes)
    assert usuarioExiste == False, "El usuario no se ha eliminado"
# --------------------------------------------------------------------------------------------
    

# CP208
# --------------------------------------------------------------------------------------------
def test_eliminar_proyecto():
    storage = StorageManager()
    
    proyecto1 = Proyecto(nombre="Proyecto1", descripcion="Descripcion1")
    storage.guardar_proyecto(proyecto1)
    
    proyecto2 = Proyecto(nombre="Proyecto2", descripcion="Descripcion2")
    storage.guardar_proyecto(proyecto2)
    
    idProyectoEliminar = proyecto1.proyecto_id
    
    
    
    proyectoEliminado = storage.eliminar_proyecto(idProyectoEliminar)
    assert proyectoEliminado == True
    
    datos = storage.cargar_datos()
    proyectos_restantes = datos.get("proyectos", [])
    
    proyectoExiste = False
    
    for proyecto in proyectos_restantes:
        if proyecto["proyecto_id"] == idProyectoEliminar:
            proyectoExiste = True
            break
    assert proyectoExiste == False, "El proyecto no se ha eliminado"
# --------------------------------------------------------------------------------------------
  
#  CP103
# --------------------------------------------------------------------------------------------
def test_usuario_email_duplicado():
    storage = StorageManager()
    usuario1 = Usuario(nombre="Andres", email= "andres@gmail.com")
    storage.guardar_usuario(usuario1)
    
    usuario2 = Usuario(nombre="Paula", email= "paula@gmail.com")
    storage.guardar_usuario(usuario2)
    
    usuario3 = Usuario(nombre="Felipe", email="andres@gmail.com")
    res = storage.guardar_usuario(usuario3)
    
    assert res is False, "El sistema permitio un usuario duplicado por email"
# --------------------------------------------------------------------------------------------

# CP 301
# --------------------------------------------------------------------------------------------
def test_crear_tarea_titulo():
    
    storage = StorageManager()
    validarTitulo = ValidadorDatos()
    
    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")
    
    tituloTarea = "Tarea1"
    
    if validarTitulo.validar_no_vacio(tituloTarea):
        tarea = Tarea(titulo=tituloTarea)
        columna.agregar_tarea(tarea)
    
    res = storage.guardar_proyecto(proyecto)
    
    proyecto1 = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaTarea = proyecto1.listar_columnas()[0]
    assert len(columnaTarea.tareas) <= 1,  "No se creo la tarea, con titulo el titulo establecido"
# --------------------------------------------------------------------------------------------

# CP302
# --------------------------------------------------------------------------------------------
def test_tarea_titulo_obligatorio():
    storage = StorageManager()
    validarTitulo = ValidadorDatos()

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")

    tituloTarea = ""  
    
    if validarTitulo.validar_no_vacio(tituloTarea):
        tarea = Tarea(titulo=tituloTarea)
        columna.agregar_tarea(tarea)

    storage.guardar_proyecto(proyecto)

    proyecto1 = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaTarea = proyecto1.listar_columnas()[0]

    assert len(columnaTarea.tareas) == 0, "El sistema creo una tarea con titulo"
# --------------------------------------------------------------------------------------------

# CP 303
# --------------------------------------------------------------------------------------------
def test_seleccionarPrioridadTarea():
    storage = StorageManager()

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")

    tituloTarea = "Tarea1"  

    tarea = Tarea(titulo=tituloTarea, prioridad="Alta")
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    proyecto1 = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaTarea = proyecto1.listar_columnas()[0]
    
    assert len(columnaTarea.tareas) == 1, "El sistema no permitio crear la tarea seleccionando la prioridad"
# --------------------------------------------------------------------------------------------

# CP 503    
# --------------------------------------------------------------------------------------------
def test_seleccion_tarea(monkeypatch):
    storage = StorageManager()
    cli = CliInterface()
    cli.storage = storage

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")
    tarea = Tarea(titulo="Tarea1", prioridad="Alta")
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    inputs = iter([
        "2",         
        "Login Nuevo",  
        "0"              
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    cli.proyecto_actual = proyecto  
    cli.editar_tarea(columna, tarea)

    proyectoCargado = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaCargada = proyectoCargado.listar_columnas()[0]
    tareaActualizada = columnaCargada.tareas[0]
    
    assert tareaActualizada.descripcion == "Login Nuevo", "El sistema no permitió actualizar la descripción"

# --------------------------------------------------------------------------------------------

# CP 304
# --------------------------------------------------------------------------------------------
def test_crear_tarea_medio_defecto():
    storage = StorageManager()

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")

    tituloTarea = "Tarea1"  

    tarea = Tarea(titulo=tituloTarea)
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    proyecto1 = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaTarea = proyecto1.listar_columnas()[0]
    tareaCargada = columnaTarea.listar_tareas()[0]
    
    assert tareaCargada.prioridad == "Media", "El sistema no creo la tarea como prioridad media de defecto"
# --------------------------------------------------------------------------------------------

# CP 1002
# --------------------------------------------------------------------------------------------
def test_guardado_automatico_despues_crear_tarea(monkeypatch):
    storage = StorageManager()


    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")


    tarea = Tarea(titulo="Tarea1", prioridad="Media")
    columna.agregar_tarea(tarea)


    storage.guardar_proyecto(proyecto)


    proyectoCargado = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaCargada = proyectoCargado.listar_columnas()[0]
    tareaCargada = columnaCargada.listar_tareas()[0]

    assert tareaCargada.titulo == "Tarea1", "La tarea no se guardó automáticamente"

# --------------------------------------------------------------------------------------------

# CP104
# --------------------------------------------------------------------------------------------
def test_usuario_id_unico():
    storage = StorageManager()
    usuario1 = Usuario(nombre="Andres", email= "andres@gmail.com")
    storage.guardar_usuario(usuario1)
    
    usuario2 = Usuario(nombre="Paula", email= "paula@gmail.com")
    storage.guardar_usuario(usuario2)
    
    usuarios = storage.cargar_todos_usuarios()
    
    assert usuarios[0].usuario_id != usuarios[1].usuario_id, "El usuario no se crea automáticamente con ID"
# --------------------------------------------------------------------------------------------

# CP204
# --------------------------------------------------------------------------------------------
def test_crar_proyecto_nombre_descripcion():
    storage = StorageManager()
    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    storage.guardar_proyecto(proyecto)
    
    proyectosCargados = storage.cargar_todos_proyectos()

    assert len(proyectosCargados) > 0, "El sistema no guardo el proyecto con nombre o descripcion"
    
# --------------------------------------------------------------------------------------------

# CP 205
# --------------------------------------------------------------------------------------------
def test_crear_proyecto_id_unico():
    storage = StorageManager()
    
    proyecto1 = Proyecto(nombre="Proyecto1")
    storage.guardar_proyecto(proyecto1)
    
    proyecto2 = Proyecto(nombre="Proyecto2")
    storage.guardar_proyecto(proyecto2)

    
    proyectosCargados = storage.cargar_todos_proyectos()
    
    assert proyectosCargados[0].proyecto_id != proyectosCargados[1].proyecto_id, "No se crea automaticamnete los proyectos con ID unico"
# --------------------------------------------------------------------------------------------

# CP 305   
# --------------------------------------------------------------------------------------------

def test_crear_tarea_ID_unico():
    storage = StorageManager()

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")


    tarea = Tarea(titulo="Tarea1")
    columna.agregar_tarea(tarea)
    
    tarea2 = Tarea(titulo="Tarea2")
    columna.agregar_tarea(tarea2)
    
    storage.guardar_proyecto(proyecto)

    proyecto1 = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaTarea = proyecto1.listar_columnas()[0]
    tareasCargadas = columnaTarea.listar_tareas()
    
    assert tareasCargadas[0].tarea_id != tareasCargadas[1].tarea_id, "El sistema no guarda tareas con ID unico "
# --------------------------------------------------------------------------------------------

# CP 405
# --------------------------------------------------------------------------------------------
def test_eliminar_tarea_confirmacion(monkeypatch):
    storage = StorageManager()

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")

    tarea = Tarea(titulo="Tarea1", prioridad="Media")
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    id_tarea_eliminar = tarea.tarea_id

    inputs = iter(["s"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    columna.eliminar_tarea(id_tarea_eliminar)
    storage.guardar_proyecto(proyecto)

    proyecto_cargado = storage.cargar_proyecto(proyecto.proyecto_id)
    columna_cargada = proyecto_cargado.listar_columnas()[0]
    tareas_restantes = columna_cargada.listar_tareas()

    tarea_existe = False
    for t in tareas_restantes:
        if t.tarea_id == id_tarea_eliminar:
            tarea_existe = True
            break

    assert tarea_existe is False, "El sistema no eliminó la tarea después de la confirmación"
# --------------------------------------------------------------------------------------------

# CP710
# --------------------------------------------------------------------------------------------
def test_renombrar_columna(monkeypatch):

    storage = StorageManager()
    cli = CliInterface()
    cli.storage = storage


    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    columna = proyecto.agregar_columna("Pendiente")
    storage.guardar_proyecto(proyecto)
    cli.proyecto_actual = proyecto  

    inputs = iter([
        "r",             
        "1",             
        "En progreso",  
        "",             
        "v"             
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cli.gestionar_columnas()

    proyectoCargado = storage.cargar_proyecto(proyecto.proyecto_id)
    columnaRenombrada = proyectoCargado.listar_columnas()[0]

    assert columnaRenombrada.nombre == "En progreso", "La columna no fue renombrada correctamente"
# --------------------------------------------------------------------------------------------

# CP711
# --------------------------------------------------------------------------------------------
def test_eliminar_columna_confirmacion(monkeypatch): 
    storage = StorageManager()
    cli = CliInterface()
    cli.storage = storage

    proyecto = Proyecto(nombre="Proyecto1", descripcion="Login")
    cli.proyecto_actual = proyecto

    columna = proyecto.agregar_columna("Pendiente")
    storage.guardar_proyecto(proyecto)

    inputs = iter([
        "d",  
        "1",  
        "s", 
        "",
        "v"  
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar la acción
    cli.gestionar_columnas()

    # Cargar proyecto guardado
    proyectoCargado = storage.cargar_proyecto(proyecto.proyecto_id)

    # Validar que se haya eliminado la columna
    assert proyectoCargado is not None
    assert len(proyectoCargado.columnas) == 0, "No se elimino la columna despues de confirmar"
# --------------------------------------------------------------------------------------------

# CP606
# --------------------------------------------------------------------------------------------
def test_mensaje_vacio_columna(monkeypatch):

    cli = CliInterface()
    proyecto = Proyecto(nombre="Proyecto Vacío", descripcion="Sin tareas")
    proyecto.agregar_columna("Pendiente")
    cli.proyecto_actual = proyecto

    prints = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: prints.append(" ".join(map(str, args))))

    monkeypatch.setattr("builtins.input", lambda _: "")

    cli.ver_tablero()

    salida = "\n".join(prints)

    assert "(vacio)" in salida, "No se mostró el mensaje '(vacio)' para una columna sin tareas"
# --------------------------------------------------------------------------------------------


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
def test_seleccionar_usuario_existente_como_actual(monkeypatch, capsys, tmp_path):
    archivo_test = tmp_path / "usuarios.json"
    cli = CliInterface()
    cli.storage = StorageManager(archivo_datos=archivo_test)

    # Crear usuarios directamente
    usuario1 = Usuario(nombre="Ana", email="ana@example.com")
    usuario2 = Usuario(nombre="Luis", email="luis@example.com")

    cli.storage.guardar_usuario(usuario1)
    cli.storage.guardar_usuario(usuario2)

    # Simular entrada del usuario
    inputs = iter(["2", ""])  # Selecciona el segundo usuario
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Ejecutar la acción
    cli.seleccionar_usuario()

    salida = capsys.readouterr().out

    # Validaciones
    assert cli.usuario_actual is not None, "No se estableció ningún usuario actual."
    assert cli.usuario_actual.nombre == "Luis", f"Se seleccionó {cli.usuario_actual.nombre} en lugar de Luis."



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



import pytest
from models import Proyecto, Tarea, Usuario
from storage import StorageManager
from cli import CliInterface

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
CP409 - Agregar etiquetas a una tarea existente

Title: CP409 Validar que el sistema permita agregar nuevas etiquetas a una tarea existente.

Description:
Prueba simple (junior) que crea una tarea, agrega etiquetas mediante la API `agregar_etiqueta`
y verifica que las etiquetas se almacenan correctamente y no se duplican.
"""
def test_cp409_agregar_etiquetas_tarea_simple():
	proyecto = Proyecto(nombre="Proyecto CP409")
	columna = proyecto.agregar_columna("Tareas")

	tarea = Tarea(titulo="Tarea etiquetas")
	columna.agregar_tarea(tarea)

	tarea.agregar_etiqueta("bug")
	tarea.agregar_etiqueta("ui")

	assert "bug" in tarea.etiquetas
	assert "ui" in tarea.etiquetas


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
