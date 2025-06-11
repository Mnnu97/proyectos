from django.urls import path, reverse_lazy

# Vistas CRUD de Proyectos y Tareas
from .views_crud import (
    # Proyectos
    ProyectoListView,
    ProyectoDetailView,
    ProyectoCreateView,
    ProyectoUpdateView,
    ProyectoDeleteView,

    # Tareas
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
from .views_usuarios import (
    lista_usuarios,
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
    asignar_proyectos,
    detalle_usuario,
    ver_proyectos_usuario,
)

# Vista para importar datos
from .views_import import importar_proyectos  # ← Importamos la vista de importar

# Exportaciones
from .views_export import exportar_todos_los_proyectos, exportar_proyectos, exportar_proyecto_individual

# Autenticación personalizada
from django.contrib.auth import views as auth_views
from .views import CustomLoginView


app_name = 'proyectos'

urlpatterns = [
    # ======================
    # 🏠 Página principal
    # ======================
    path('', PaginaInicioView.as_view(), name='inicio'),

    # ======================
    # 📁 PROYECTOS
    # ======================
    path('proyectos/', ProyectoListView.as_view(), name='proyecto_list'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_delete'),

    # Estado del proyecto
    path('proyectos/<int:pk>/estado/', actualizar_estado_proyecto, name='actualizar_estado_proyecto'),

    # ======================
    # 📝 TAREAS
    # ======================
    path('tareas/', TareaListView.as_view(), name='tarea_list'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_create_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_update_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_delete_en_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/<int:tarea_id>/estado/', actualizar_estado_tarea, name='actualizar_estado_tarea_en_proyecto'),

    # ======================
    # 📦 EXPORTACIONES
    # ======================
    path('proyectos/exportar-completo/', exportar_todos_los_proyectos, name='exportar_todos_los_proyectos'),
    path('proyectos/exportar/', exportar_proyectos, name='exportar_proyectos'),
    path('proyectos/<int:pk>/exportar/', exportar_proyecto_individual, name='exportar_proyecto_individual'),

    # ======================
    # 📤 IMPORTACIÓN DE DATOS (NUEVA RUTA)
    # ======================
    path('proyectos/importar/', importar_proyectos, name='importar_proyectos'),  # ✅ Botón Importar ahora funciona

    # ======================
    # 🔐 AUTENTICACIÓN
    # ======================
    path('login/', CustomLoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', signup, name='registro'),

    path('cambiar-password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('proyectos:password_change_done')
    ), name='password_change'),
    path('cambiar-password/hecho/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),

    # ======================
    # 👥 PANEL DE USUARIOS (Admin)
    # ======================
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/asignar-proyectos/', asignar_proyectos, name='asignar_proyectos'),
    path('usuarios/<int:pk>/detalles/', detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/proyectos/', ver_proyectos_usuario, name='ver_proyectos_usuario'),
]