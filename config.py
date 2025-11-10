"""
Configuración del Proyecto Trello Manager
Define constantes y configuraciones globales
"""

import os
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "projects.json"

# Crear directorio de datos si no existe
DATA_DIR.mkdir(exist_ok=True)

# Constantes de estado
TASK_STATUS_PENDING = "Pendiente"
TASK_STATUS_IN_PROGRESS = "En Progreso"
TASK_STATUS_COMPLETED = "Completada"
TASK_STATUS_BLOCKED = "Bloqueada"

TASK_STATUSES = [
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_BLOCKED
]

# Constantes de prioridad
PRIORITY_LOW = "Baja"
PRIORITY_MEDIUM = "Media"
PRIORITY_HIGH = "Alta"
PRIORITY_URGENT = "Urgente"

PRIORITIES = [
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_HIGH,
    PRIORITY_URGENT
]

# Configuración de colores para CLI (ANSI)
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}

def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"{COLORS['BOLD']}{COLORS['CYAN']}{text}{COLORS['END']}")

def print_success(text):
    """Imprime un mensaje de éxito"""
    print(f"{COLORS['GREEN']}✓ {text}{COLORS['END']}")

def print_error(text):
    """Imprime un mensaje de error"""
    print(f"{COLORS['RED']}✗ {text}{COLORS['END']}")

def print_warning(text):
    """Imprime un mensaje de advertencia"""
    print(f"{COLORS['YELLOW']}⚠ {text}{COLORS['END']}")

def print_info(text):
    """Imprime un mensaje de información"""
    print(f"{COLORS['BLUE']}ℹ {text}{COLORS['END']}")
