import pytest
from models import Usuario
from utils import ValidadorDatos
from storage import StorageManager
from cli import CliInterface

def test_validar_correo():
    correoValidar = ValidadorDatos()
    validacion = correoValidar.validar_email("andres@gmail.com")
    assert validacion == True

def test_eliminar_usuario_id(monkeypatch):
    cli = CliInterface()
    cli.storage.cargar_todos_usuarios = lambda: [
        Usuario(usuario_id="1", nombre="Andrés", email="andres@example.com"),
        Usuario(usuario_id="2", nombre="Laura", email="laura@example.com"),
    ]
    cli.storage.eliminar_usuario = lambda usuario_id: True 
    res = iter(["1", "s", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(res))
    cli.eliminar_usuario()
    assert cli.storage.eliminar_usuario(1) == True
    
