"""
Punto de entrada principal de la aplicación
Project Manager - Gestor de Proyectos y Tareas
"""

from cli import CliInterface


def main():
    """Función principal"""
    app = CliInterface()
    try:
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n")
        print("\033[93m" + "⚠ Aplicación interrumpida por el usuario" + "\033[0m")
    except Exception as e:
        print(f"\033[91m✗ Error: {e}\033[0m")


if __name__ == "__main__":
    main()
