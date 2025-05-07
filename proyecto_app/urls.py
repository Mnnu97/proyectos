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

    # 🔸 Rutas para Tareas
    path('tareas/', TareaListView.as_view(), name='tarea_list'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    path('tareas/crear/', TareaCreateView.as_view(), name='tarea_create'),
    path('tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_update'),
    path('tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_delete'),

    #  Accion para actualizar
    path('tareas/<int:pk>/estado/', actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('proyectos/<int:pk>/estado/', actualizar_estado_proyecto, name='actualizar_estado_proyecto'),

    # usuario
    path('registro/', signup, name='signup'),
]