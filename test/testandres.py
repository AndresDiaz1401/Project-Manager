import pytest
from utils import ValidadorDatos

def test_validar_correo():
    correoValidar = ValidadorDatos()
    correoValidar.validar_email("andres@gmail.com")
    assert correoValidar == True
    