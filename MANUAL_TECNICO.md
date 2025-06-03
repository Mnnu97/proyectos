Sistema de Gestión de Proyectos

## Descripción

Aplicación web desarrollada en Django para la gestión de proyectos y tareas, con administración de usuarios y exportación de datos.

## Requisitos

- Python 3.8+
- Django 4.x
- PostgreSQL
- Paquetes listados en `requirements.txt`

## Instalación

1. Clona el repositorio:
   ```sh
   git clone <URL-del-repositorio>
   cd Gestion-de-Proyectos
   ```

2. Crea y activa un entorno virtual:
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

3. Instala dependencias:
   ```sh
   pip install -r requirements.txt
   ```

4. Configura la base de datos en `proyectos/settings.py`:
   - Cambia los valores de `NAME`, `USER` y `PASSWORD` según tu configuración de PostgreSQL.

5. Aplica migraciones:
   ```sh
   python manage.py migrate
   ```

6. Crea un superusuario:
   ```sh
   python manage.py createsuperuser
   ```

7. Ejecuta el servidor:
   ```sh
   python manage.py runserver
   ```

## Estructura del Proyecto

- `proyecto_app/`: Lógica principal, modelos, vistas, formularios y administración.
- `proyectos/`: Configuración global de Django.
- `templates/`: Plantillas HTML.
- `static/`: Archivos estáticos (CSS, JS, imágenes).

## Modelos principales

- **Proyecto:** nombre, descripción, fechas, estado, usuarios asignados.
- **Tarea:** título, descripción, proyecto, usuario asignado, estado.

## Administración

- Personalización del panel de administración para gestionar proyectos y tareas.
- Búsqueda, filtros y ordenación en el admin.

## Pruebas

Ejecuta los tests con:
```sh
python manage.py test
```

## Mantenimiento

- Para actualizar dependencias:  
  ```sh
  pip install -r requirements.txt
  ```
- Para crear nuevas migraciones:
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```