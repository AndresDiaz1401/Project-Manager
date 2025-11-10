"""
Interfaz de linea de comandos interactiva
Proporciona menus y opciones para gestionar proyectos y tareas
"""

import os
import sys
from typing import Optional

from config import (
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_BLOCKED,
    PRIORITIES,
)
from models import Proyecto, Usuario, Columna, Tarea
from storage import StorageManager


class CliInterface:
    """Interfaz de linea de comandos para gestionar proyectos"""

    def __init__(self):
        self.storage = StorageManager()
        self.usuario_actual: Optional[Usuario] = None
        self.proyecto_actual: Optional[Proyecto] = None

    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal"""
        os.system("clear" if os.name == "posix" else "cls")

    def mostrar_menu_principal(self):
        """Muestra el menu principal"""
        self.limpiar_pantalla()
        print_header("+--------------------------------------+")
        print_header("|       PROJECT MANAGER v1.0           |")
        print_header("|   Gestor de Proyectos y Tareas       |")
        print_header("+--------------------------------------+")
        print()
        print("MENU PRINCIPAL")
        print("-" * 40)
        print("1. Gestionar Usuarios")
        print("2. Gestionar Proyectos")
        print("3. Trabajar con Proyecto Actual")
        print("4. Salir")
        print()
        return input("Seleccione una opcion (1-4): ").strip()

    def mostrar_menu_usuarios(self):
        """Menu para gestionar usuarios"""
        opcion = None
        while opcion != "5":
            self.limpiar_pantalla()
            print_header("GESTION DE USUARIOS")
            print()
            print("1. Crear nuevo usuario")
            print("2. Listar usuarios")
            print("3. Seleccionar usuario actual")
            print("4. Eliminar usuario")
            print("5. Volver al menu principal")
            print()
            opcion = input("Seleccione una opcion (1-5): ").strip()

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.seleccionar_usuario()
            elif opcion == "4":
                self.eliminar_usuario()
            elif opcion == "5":
                continue
            else:
                print_error("Opcion no valida")
                input("Presione Enter para continuar...")

    def crear_usuario(self):
        """Crea un nuevo usuario"""
        print()
        nombre = input("Nombre del usuario: ").strip()
        if not nombre:
            print_error("El nombre no puede estar vacio")
            return

        email = input("Email del usuario: ").strip()
        if not email or "@" not in email:
            print_error("Email invalido")
            return

        usuario = Usuario(nombre, email)
        if self.storage.guardar_usuario(usuario):
            print_success(f"Usuario '{nombre}' creado exitosamente")
        else:
            print_error("Error al crear el usuario")

        input("Presione Enter para continuar...")

    def listar_usuarios(self):
        """Lista todos los usuarios"""
        usuarios = self.storage.cargar_todos_usuarios()

        if not usuarios:
            print_warning("No hay usuarios registrados")
        else:
            print()
            print_header("USUARIOS REGISTRADOS")
            print("-" * 60)
            for i, usuario in enumerate(usuarios, 1):
                marcado = (
                    " *"
                    if self.usuario_actual
                    and usuario.usuario_id == self.usuario_actual.usuario_id
                    else ""
                )
                print(f"{i}. {usuario.nombre:<20} | {usuario.email:<25} {marcado}")

        input("Presione Enter para continuar...")

    def seleccionar_usuario(self):
        """Selecciona el usuario actual"""
        usuarios = self.storage.cargar_todos_usuarios()

        if not usuarios:
            print_warning("No hay usuarios disponibles")
            input("Presione Enter para continuar...")
            return

        print()
        print_header("SELECCIONAR USUARIO")
        print("-" * 40)
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario.nombre} ({usuario.email})")

        print()
        try:
            opcion = int(input("Seleccione el numero del usuario: ").strip())
            if 1 <= opcion <= len(usuarios):
                self.usuario_actual = usuarios[opcion - 1]
                print_success(f"Usuario actual: {self.usuario_actual.nombre}")
            else:
                print_error("Opcion no valida")
        except ValueError:
            print_error("Debe ingresar un numero")

        input("Presione Enter para continuar...")

    def eliminar_usuario(self):
        """Elimina un usuario"""
        usuarios = self.storage.cargar_todos_usuarios()

        if not usuarios:
            print_warning("No hay usuarios para eliminar")
            input("Presione Enter para continuar...")
            return

        print()
        print_header("ELIMINAR USUARIO")
        print("-" * 40)
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. {usuario.nombre}")

        print()
        try:
            opcion = int(input("Seleccione el usuario a eliminar: ").strip())
            if 1 <= opcion <= len(usuarios):
                usuario = usuarios[opcion - 1]
                confirmacion = input(f"Eliminar '{usuario.nombre}'? (s/n): ").lower()
                if confirmacion == "s":
                    if self.storage.eliminar_usuario(usuario.usuario_id):
                        print_success("Usuario eliminado")
                        if (
                            self.usuario_actual
                            and self.usuario_actual.usuario_id == usuario.usuario_id
                        ):
                            self.usuario_actual = None
                    else:
                        print_error("Error al eliminar el usuario")
            else:
                print_error("Opcion no valida")
        except ValueError:
            print_error("Debe ingresar un numero")

        input("Presione Enter para continuar...")

    def mostrar_menu_proyectos(self):
        """Menu para gestionar proyectos"""
        opcion = None
        while opcion != "5":
            self.limpiar_pantalla()
            print_header("GESTION DE PROYECTOS")
            print()
            print("1. Crear nuevo proyecto")
            print("2. Listar proyectos")
            print("3. Abrir proyecto")
            print("4. Eliminar proyecto")
            print("5. Volver al menu principal")
            print()
            opcion = input("Seleccione una opcion (1-5): ").strip()

            if opcion == "1":
                self.crear_proyecto()
            elif opcion == "2":
                self.listar_proyectos()
            elif opcion == "3":
                self.abrir_proyecto()
            elif opcion == "4":
                self.eliminar_proyecto()
            elif opcion == "5":
                continue
            else:
                print_error("Opcion no valida")
                input("Presione Enter para continuar...")

    def crear_proyecto(self):
        """Crea un nuevo proyecto"""
        print()
        nombre = input("Nombre del proyecto: ").strip()
        if not nombre:
            print_error("El nombre no puede estar vacio")
            input("Presione Enter para continuar...")
            return

        descripcion = input("Descripcion del proyecto (opcional): ").strip()

        propietario_id = self.usuario_actual.usuario_id if self.usuario_actual else None
        proyecto = Proyecto(nombre, descripcion, propietario_id)

        # Agregar columnas por defecto
        proyecto.agregar_columna("Pendiente")
        proyecto.agregar_columna("En Progreso")
        proyecto.agregar_columna("Completada")

        if self.storage.guardar_proyecto(proyecto):
            print_success(f"Proyecto '{nombre}' creado exitosamente")
        else:
            print_error("Error al crear el proyecto")

        input("Presione Enter para continuar...")

    def listar_proyectos(self):
        """Lista todos los proyectos"""
        proyectos = self.storage.cargar_todos_proyectos()

        if not proyectos:
            print_warning("No hay proyectos registrados")
        else:
            print()
            print_header("PROYECTOS DISPONIBLES")
            print("-" * 80)
            for i, proyecto in enumerate(proyectos, 1):
                tareas = proyecto.contar_tareas()
                columnas = len(proyecto.columnas)
                marcado = (
                    " *"
                    if self.proyecto_actual
                    and proyecto.proyecto_id == self.proyecto_actual.proyecto_id
                    else ""
                )
                print(
                    f"{i}. {proyecto.nombre:<25} | {tareas} tareas | {columnas} columnas {marcado}"
                )

        input("Presione Enter para continuar...")

    def abrir_proyecto(self):
        """Abre un proyecto para trabajar con el"""
        proyectos = self.storage.cargar_todos_proyectos()

        if not proyectos:
            print_warning("No hay proyectos disponibles")
            input("Presione Enter para continuar...")
            return

        print()
        print_header("SELECCIONAR PROYECTO")
        print("-" * 40)
        for i, proyecto in enumerate(proyectos, 1):
            print(f"{i}. {proyecto.nombre}")

        print()
        try:
            opcion = int(input("Seleccione el proyecto: ").strip())
            if 1 <= opcion <= len(proyectos):
                self.proyecto_actual = proyectos[opcion - 1]
                print_success(f"Proyecto actual: {self.proyecto_actual.nombre}")
            else:
                print_error("Opcion no valida")
        except ValueError:
            print_error("Debe ingresar un numero")

        input("Presione Enter para continuar...")

    def eliminar_proyecto(self):
        """Elimina un proyecto"""
        proyectos = self.storage.cargar_todos_proyectos()

        if not proyectos:
            print_warning("No hay proyectos para eliminar")
            input("Presione Enter para continuar...")
            return

        print()
        print_header("ELIMINAR PROYECTO")
        print("-" * 40)
        for i, proyecto in enumerate(proyectos, 1):
            print(f"{i}. {proyecto.nombre}")

        print()
        try:
            opcion = int(input("Seleccione el proyecto a eliminar: ").strip())
            if 1 <= opcion <= len(proyectos):
                proyecto = proyectos[opcion - 1]
                confirmacion = input(f"Eliminar '{proyecto.nombre}'? (s/n): ").lower()
                if confirmacion == "s":
                    if self.storage.eliminar_proyecto(proyecto.proyecto_id):
                        print_success("Proyecto eliminado")
                        if (
                            self.proyecto_actual
                            and self.proyecto_actual.proyecto_id == proyecto.proyecto_id
                        ):
                            self.proyecto_actual = None
                    else:
                        print_error("Error al eliminar el proyecto")
            else:
                print_error("Opcion no valida")
        except ValueError:
            print_error("Debe ingresar un numero")

        input("Presione Enter para continuar...")

    def mostrar_menu_proyecto_actual(self):
        """Menu para trabajar con el proyecto actual"""
        if not self.proyecto_actual:
            print_error("No hay proyecto seleccionado")
            input("Presione Enter para continuar...")
            return

        opcion = None
        while opcion != "6":
            self.limpiar_pantalla()
            print_header(f"PROYECTO: {self.proyecto_actual.nombre}")
            print(f"Total de tareas: {self.proyecto_actual.contar_tareas()}")
            print()
            print("1. Ver tablero")
            print("2. Agregar tarea")
            print("3. Buscar tarea")
            print("4. Gestionar columnas")
            print("5. Ver estadisticas")
            print("6. Volver al menu principal")
            print()
            opcion = input("Seleccione una opcion (1-6): ").strip()

            if opcion == "1":
                self.ver_tablero()
            elif opcion == "2":
                self.agregar_tarea()
            elif opcion == "3":
                self.buscar_tarea()
            elif opcion == "4":
                self.gestionar_columnas()
            elif opcion == "5":
                self.ver_estadisticas()
            elif opcion == "6":
                continue
            else:
                print_error("Opcion no valida")
                input("Presione Enter para continuar...")

    def ver_tablero(self):
        """Visualiza el tablero del proyecto"""
        self.limpiar_pantalla()
        print_header(f"TABLERO: {self.proyecto_actual.nombre}")
        print()

        columnas = self.proyecto_actual.listar_columnas()
        if not columnas:
            print_warning("No hay columnas en el proyecto")
        else:
            for columna in columnas:
                print_header(f"+- {columna.nombre} ({columna.contar_tareas()} tareas)")
                print("-" * 40)

                if not columna.tareas:
                    print("| (vacio)")
                else:
                    for tarea in columna.tareas:
                        prioridad_icon = {
                            "Urgente": "!!",
                            "Alta": "[A]",
                            "Media": "[M]",
                            "Baja": "[B]",
                        }.get(tarea.prioridad, "[ ]")
                        print(f"| {prioridad_icon} {tarea.titulo}")
                        print(
                            f"|    ID: {tarea.tarea_id[:8]}... | Asignado: {tarea.asignado_a or 'Sin asignar'}"
                        )

                print("+" + "-" * 39)
                print()

        input("Presione Enter para continuar...")

    def agregar_tarea(self):
        """Agrega una nueva tarea al proyecto"""
        columnas = self.proyecto_actual.listar_columnas()

        if not columnas:
            print_error("No hay columnas en el proyecto")
            input("Presione Enter para continuar...")
            return

        print()
        print_header("AGREGAR NUEVA TAREA")
        print("-" * 40)

        titulo = input("Titulo de la tarea: ").strip()
        if not titulo:
            print_error("El titulo no puede estar vacio")
            input("Presione Enter para continuar...")
            return

        descripcion = input("Descripcion (opcional): ").strip()

        print()
        print("Prioridades disponibles:")
        for i, prioridad in enumerate(PRIORITIES, 1):
            print(f"{i}. {prioridad}")

        try:
            opcion_prioridad = int(input("Seleccione prioridad: ").strip())
            prioridad = (
                PRIORITIES[opcion_prioridad - 1]
                if 1 <= opcion_prioridad <= len(PRIORITIES)
                else "Media"
            )
        except (ValueError, IndexError):
            prioridad = "Media"

        print()
        print("Seleccione columna:")
        for i, columna in enumerate(columnas, 1):
            print(f"{i}. {columna.nombre}")

        try:
            opcion_columna = int(input("Seleccione columna: ").strip())
            if not (1 <= opcion_columna <= len(columnas)):
                print_error("Opcion no valida")
                return
            columna = columnas[opcion_columna - 1]
        except ValueError:
            print_error("Debe ingresar un numero")
            return

        asignado_a = (
            input("Asignar a usuario (opcional, nombre o ID): ").strip() or None
        )

        tarea = Tarea(titulo, descripcion, prioridad, asignado_a)
        columna.agregar_tarea(tarea)

        if self.storage.guardar_proyecto(self.proyecto_actual):
            print_success(f"Tarea '{titulo}' agregada a '{columna.nombre}'")
        else:
            print_error("Error al agregar la tarea")

        input("Presione Enter para continuar...")

    def buscar_tarea(self):
        """Busca una tarea por titulo"""
        print()
        termino = (
            input("Ingrese el titulo o parte de el para buscar: ").strip().lower()
        )

        if not termino:
            print_error("El termino de busqueda no puede estar vacio")
            input("Presione Enter para continuar...")
            return

        tareas_encontradas = []
        for columna in self.proyecto_actual.columnas:
            for tarea in columna.tareas:
                if (
                    termino in tarea.titulo.lower()
                    or termino in tarea.descripcion.lower()
                ):
                    tareas_encontradas.append((columna, tarea))

        print()
        if not tareas_encontradas:
            print_warning("No se encontraron tareas")
        else:
            print_header(
                f"RESULTADOS DE BUSQUEDA: {len(tareas_encontradas)} tareas encontradas"
            )
            print("-" * 60)
            for i, (columna, tarea) in enumerate(tareas_encontradas, 1):
                print(f"{i}. {tarea.titulo} (en '{columna.nombre}')")
                print(
                    f"   Prioridad: {tarea.prioridad} | Asignado: {tarea.asignado_a or 'Sin asignar'}"
                )

            print()
            try:
                opcion = int(
                    input("Seleccione tarea para editar (0 para cancelar): ").strip()
                )
                if 1 <= opcion <= len(tareas_encontradas):
                    columna, tarea = tareas_encontradas[opcion - 1]
                    self.editar_tarea(columna, tarea)
            except ValueError:
                pass

        input("Presione Enter para continuar...")

    def editar_tarea(self, columna: Columna, tarea: Tarea):
        """Edita una tarea existente"""
        continuar = True
        while continuar:
            print()
            print_header(f"EDITAR TAREA: {tarea.titulo}")
            print(f"Columna: {columna.nombre}")
            print("-" * 40)
            print("1. Cambiar titulo")
            print("2. Cambiar descripcion")
            print("3. Cambiar prioridad")
            print("4. Cambiar estado")
            print("5. Asignar a usuario")
            print("6. Mover a otra columna")
            print("7. Agregar etiqueta")
            print("8. Ver detalles")
            print("9. Eliminar tarea")
            print("0. Guardar y volver")
            print()
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                nuevo_titulo = input("Nuevo titulo: ").strip()
                if nuevo_titulo:
                    tarea.actualizar(titulo=nuevo_titulo)
            elif opcion == "2":
                nueva_desc = input("Nueva descripcion: ").strip()
                tarea.actualizar(descripcion=nueva_desc)
            elif opcion == "3":
                print("Prioridades:")
                for i, p in enumerate(PRIORITIES, 1):
                    print(f"{i}. {p}")
                try:
                    op = int(input("Seleccione prioridad: ").strip())
                    if 1 <= op <= len(PRIORITIES):
                        tarea.actualizar(prioridad=PRIORITIES[op - 1])
                except ValueError:
                    pass
            elif opcion == "4":
                print("Estados:")
                estados = [
                    TASK_STATUS_PENDING,
                    TASK_STATUS_IN_PROGRESS,
                    TASK_STATUS_COMPLETED,
                    TASK_STATUS_BLOCKED,
                ]
                for i, estado in enumerate(estados, 1):
                    print(f"{i}. {estado}")
                try:
                    op = int(input("Seleccione estado: ").strip())
                    if 1 <= op <= len(estados):
                        tarea.actualizar(estado=estados[op - 1])
                except ValueError:
                    pass
            elif opcion == "5":
                nuevo_usuario = input("Asignar a (nombre o ID): ").strip() or None
                tarea.actualizar(asignado_a=nuevo_usuario)
            elif opcion == "6":
                columnas = self.proyecto_actual.listar_columnas()
                print("Columnas disponibles:")
                for i, c in enumerate(columnas, 1):
                    print(f"{i}. {c.nombre}")
                try:
                    op = int(input("Seleccione columna de destino: ").strip())
                    if 1 <= op <= len(columnas):
                        nueva_columna = columnas[op - 1]
                        columna.eliminar_tarea(tarea.tarea_id)
                        nueva_columna.agregar_tarea(tarea)
                        columna = nueva_columna
                        print_success("Tarea movida")
                except ValueError:
                    pass
            elif opcion == "7":
                etiqueta = input("Etiqueta a agregar: ").strip()
                if etiqueta:
                    tarea.agregar_etiqueta(etiqueta)
                    print_success("Etiqueta agregada")
            elif opcion == "8":
                print()
                print_info(f"ID: {tarea.tarea_id}")
                print_info(f"Titulo: {tarea.titulo}")
                print_info(f"Descripcion: {tarea.descripcion}")
                print_info(f"Prioridad: {tarea.prioridad}")
                print_info(f"Estado: {tarea.estado}")
                print_info(f"Asignado a: {tarea.asignado_a or 'Sin asignar'}")
                print_info(
                    f"Etiquetas: {', '.join(tarea.etiquetas) if tarea.etiquetas else 'Sin etiquetas'}"
                )
                print_info(f"Creada: {tarea.fecha_creacion}")
                print_info(f"Modificada: {tarea.fecha_modificacion}")
            elif opcion == "9":
                confirmacion = input(
                    f"Eliminar tarea '{tarea.titulo}'? (s/n): "
                ).lower()
                if confirmacion == "s":
                    columna.eliminar_tarea(tarea.tarea_id)
                    print_success("Tarea eliminada")
                    continuar = False
            elif opcion == "0":
                self.storage.guardar_proyecto(self.proyecto_actual)
                print_success("Cambios guardados")
                continuar = False
            else:
                print_error("Opcion no valida")

    def gestionar_columnas(self):
        """Gestiona las columnas del proyecto"""
        opcion = ""
        while opcion != "v":
            self.limpiar_pantalla()
            print_header("GESTIONAR COLUMNAS")
            print()
            columnas = self.proyecto_actual.listar_columnas()

            for i, columna in enumerate(columnas, 1):
                print(f"{i}. {columna.nombre} ({columna.contar_tareas()} tareas)")

            print()
            print("a. Agregar columna")
            print("r. Renombrar columna")
            print("d. Eliminar columna")
            print("v. Volver")
            print()
            opcion = input("Seleccione una opcion: ").strip().lower()

            if opcion == "a":
                nombre = input("Nombre de la nueva columna: ").strip()
                if nombre:
                    self.proyecto_actual.agregar_columna(nombre)
                    self.storage.guardar_proyecto(self.proyecto_actual)
                    print_success("Columna agregada")
                    input("Presione Enter para continuar...")
            elif opcion == "r":
                try:
                    op = int(input("Numero de columna a renombrar: ").strip())
                    if 1 <= op <= len(columnas):
                        nuevo_nombre = input("Nuevo nombre: ").strip()
                        if nuevo_nombre:
                            columnas[op - 1].nombre = nuevo_nombre
                            self.storage.guardar_proyecto(self.proyecto_actual)
                            print_success("Columna renombrada")
                    input("Presione Enter para continuar...")
                except ValueError:
                    pass
            elif opcion == "d":
                try:
                    op = int(input("Numero de columna a eliminar: ").strip())
                    if 1 <= op <= len(columnas):
                        confirmacion = input(
                            f"Eliminar '{columnas[op - 1].nombre}'? (s/n): "
                        ).lower()
                        if confirmacion == "s":
                            self.proyecto_actual.eliminar_columna(
                                columnas[op - 1].columna_id
                            )
                            self.storage.guardar_proyecto(self.proyecto_actual)
                            print_success("Columna eliminada")
                    input("Presione Enter para continuar...")
                except ValueError:
                    pass

    def ver_estadisticas(self):
        """Muestra estadisticas del proyecto"""
        self.limpiar_pantalla()
        print_header(f"ESTADISTICAS: {self.proyecto_actual.nombre}")
        print()

        todas_tareas = self.proyecto_actual.obtener_todas_las_tareas()
        total_tareas = len(todas_tareas)

        if total_tareas == 0:
            print_warning("No hay tareas en el proyecto")
            input("Presione Enter para continuar...")
            return

        # Contar por estado
        pendientes = sum(1 for t in todas_tareas if t.estado == TASK_STATUS_PENDING)
        en_progreso = sum(
            1 for t in todas_tareas if t.estado == TASK_STATUS_IN_PROGRESS
        )
        completadas = sum(1 for t in todas_tareas if t.estado == TASK_STATUS_COMPLETED)
        bloqueadas = sum(1 for t in todas_tareas if t.estado == TASK_STATUS_BLOCKED)

        # Contar por prioridad
        urgentes = sum(1 for t in todas_tareas if t.prioridad == "Urgente")
        altas = sum(1 for t in todas_tareas if t.prioridad == "Alta")
        medias = sum(1 for t in todas_tareas if t.prioridad == "Media")
        bajas = sum(1 for t in todas_tareas if t.prioridad == "Baja")

        # Tareas asignadas
        asignadas = sum(1 for t in todas_tareas if t.asignado_a)
        sin_asignar = total_tareas - asignadas

        print_info(f"Total de tareas: {total_tareas}")
        print()
        print_header("POR ESTADO:")
        print(f"  Pendiente: {pendientes} ({pendientes*100//total_tareas}%)")
        print(f"  En Progreso: {en_progreso} ({en_progreso*100//total_tareas}%)")
        print(f"  Completada: {completadas} ({completadas*100//total_tareas}%)")
        print(f"  Bloqueada: {bloqueadas} ({bloqueadas*100//total_tareas}%)")
        print()
        print_header("POR PRIORIDAD:")
        print(f"  Urgente: {urgentes} ({urgentes*100//total_tareas}%)")
        print(f"  Alta: {altas} ({altas*100//total_tareas}%)")
        print(f"  Media: {medias} ({medias*100//total_tareas}%)")
        print(f"  Baja: {bajas} ({bajas*100//total_tareas}%)")
        print()
        print_header("ASIGNACION:")
        print(f"  Asignadas: {asignadas} ({asignadas*100//total_tareas}%)")
        print(f"  Sin asignar: {sin_asignar} ({sin_asignar*100//total_tareas}%)")
        print()
        print_header("POR COLUMNA:")
        for columna in self.proyecto_actual.listar_columnas():
            print(f"  {columna.nombre}: {columna.contar_tareas()} tareas")

        input("Presione Enter para continuar...")

    def ejecutar(self):
        """Ejecuta la interfaz principal"""
        opcion = None
        while opcion != "4":
            opcion = self.mostrar_menu_principal()

            if opcion == "1":
                self.mostrar_menu_usuarios()
            elif opcion == "2":
                self.mostrar_menu_proyectos()
            elif opcion == "3":
                self.mostrar_menu_proyecto_actual()
            elif opcion == "4":
                self.limpiar_pantalla()
                print_success("Hasta luego!")
            else:
                print_error("Opcion no valida")
                input("Presione Enter para continuar...")
