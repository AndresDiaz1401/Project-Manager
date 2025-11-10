# Arquitectura del Proyecto

## Descripción General

Project Manager implementa el patrón Kanban con arquitectura orientada a objetos bien estructurada.

## Clases Principales

### Usuario

- usuario_id, nombre, email, fecha_creacion
- Métodos: to_dict(), from_dict()

### Tarea

- tarea_id, titulo, descripcion, prioridad, estado, asignado_a, etiquetas
- Métodos: actualizar(), agregar_etiqueta(), eliminar_etiqueta(), to_dict(), from_dict()

### Columna

- columna_id, nombre, orden, tareas
- Métodos: agregar_tarea(), eliminar_tarea(), obtener_tarea(), listar_tareas(), contar_tareas()

### Proyecto

- proyecto_id, nombre, descripcion, propietario_id, columnas, miembros
- Métodos: agregar_columna(), eliminar_columna(), obtener_columna(), agregar_miembro(), obtener_todas_las_tareas()

## Patrones Implementados

1. Repository Pattern - StorageManager abstrae la persistencia
2. Factory Pattern - Métodos from_dict() para deserialización
3. Composite Pattern - Estructura jerárquica
4. Strategy Pattern - Múltiples exportadores
5. Programación Orientada a Objetos

## Capas de Arquitectura

```
┌─────────────────────────────────┐
│   CLI Interface (cli.py)        │
├─────────────────────────────────┤
│   Models (models.py)            │
├─────────────────────────────────┤
│   Storage (storage.py)          │
├─────────────────────────────────┤
│   JSON Database                 │
└─────────────────────────────────┘
```

Para documentación completa, consulta los archivos del proyecto.
