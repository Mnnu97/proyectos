# Sistema de Gestión de Proyectos

Este es un sistema web para la gestión de proyectos y tareas, desarrollado con Django. Permite a los administradores y usuarios gestionar proyectos, asignar tareas, exportar información y controlar el avance de los trabajos.

## Características principales

- Gestión de proyectos (crear, editar, eliminar, listar)
- Gestión de tareas asociadas a proyectos
- Asignación de usuarios a proyectos y tareas
- Panel de administración para usuarios tipo Admin
- Exportación de proyectos a Excel
- Control de estados de proyectos y tareas
- Autenticación y registro de usuarios

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

3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

4. Configura la base de datos en `proyectos/settings.py`.

5. Aplica las migraciones:
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

## Uso

- Accede a `http://localhost:8000/` para ver la página de inicio.
- Inicia sesión o regístrate.
- Los usuarios Admin pueden gestionar usuarios y asignar proyectos.
- Los usuarios pueden ver y gestionar sus proyectos y tareas asignadas.

## Estructura del proyecto

- `proyecto_app/`: Aplicación principal con modelos, vistas y templates.
- `proyectos/`: Configuración global del proyecto Django.
- `templates/`: Plantillas HTML globales y de la app.
- `static/`: Archivos estáticos (CSS, JS, imágenes).

## Licencia

Este proyecto es solo para fines educativos.
