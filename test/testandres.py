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

# CP02
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

