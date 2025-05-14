# proyecto_app/urls.py

from django.urls import path

# Vistas CRUD
from .views_crud import (
    ProyectoListView,
    ProyectoDetailView,
    ProyectoCreateView,
    ProyectoUpdateView,
    ProyectoDeleteView,
    TareaListView,
    TareaDetailView,
    TareaCreateView,
    TareaUpdateView,
    TareaDeleteView,
)

# Otras vistas
from .views_inicio import PaginaInicioView
from .views_auth import signup
from .views_estado import actualizar_estado_tarea, actualizar_estado_proyecto

# 👇 Vistas de gestión de usuarios (Admin)
from .views_usuarios import lista_usuarios, crear_usuario, eliminar_usuario, asignar_proyectos, detalle_usuario, ver_proyectos_usuario

app_name = 'proyectos'

urlpatterns = [
    # 🏠 Ruta raíz → /proyectos/
    path('', PaginaInicioView.as_view(), name='inicio'),

    # 🔹 Rutas para Proyectos
    path('proyectos/', ProyectoListView.as_view(), name='proyecto_list'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_delete'),

    # 📝 Nuevas rutas para tareas por proyecto
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_create_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_update_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_delete_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/estado/', actualizar_estado_tarea, name='actualizar_estado_tarea_en_proyecto'),

    # 🔸 Rutas independientes para tareas (opcional)
    path('tareas/', TareaListView.as_view(), name='tarea_list'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    path('tareas/crear/', TareaCreateView.as_view(), name='tarea_create'),
    path('tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_update'),
    path('tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_delete'),
    path('tareas/<int:pk>/estado/', actualizar_estado_tarea, name='actualizar_estado_tarea'),

    # 🔁 Acciones de estado de proyectos
    path('proyectos/<int:pk>/estado/', actualizar_estado_proyecto, name='actualizar_estado_proyecto'),

    # 👤 Registro de usuario
    path('registro/', signup, name='signup'),

    # 👥 Panel de gestión de usuarios (solo Admin)
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    
    # ✅ Eliminar y Asignar Proyectos
    path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/asignar-proyectos/', asignar_proyectos, name='asignar_proyectos'),
    path('usuarios/<int:pk>/detalles/', detalle_usuario, name='detalle_usuario'),
    
    # 👀 Ver Proyectos asignados al usuario
    path('usuarios/<int:pk>/proyectos/', ver_proyectos_usuario, name='ver_proyectos_usuario'),
]