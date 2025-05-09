# proyecto_app/urls.py

from django.urls import path

# Vistas CRUD para Proyectos y Tareas
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

# Vistas adicionales
from .views_auth import signup
from .views_estado import actualizar_estado_tarea, actualizar_estado_proyecto

app_name = 'proyectos'

urlpatterns = [
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
]