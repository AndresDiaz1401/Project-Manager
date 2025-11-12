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


