from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

from .models import Proyecto, Tarea

# Función auxiliar para verificar si el usuario es Admin
def es_admin(user):
    return user.groups.filter(name='Admin').exists()

# =============================
# Vistas de estado (ya existentes)
# =============================
def actualizar_estado_proyecto(request, pk):
    """
    Cambia manualmente el estado del proyecto (pendiente/en progreso/completado)
    """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    nuevo_estado = request.GET.get('estado')

    estados_validos = dict(Proyecto.ESTADOS).keys()

    if nuevo_estado in estados_validos:
        proyecto.estado = nuevo_estado
        proyecto.save(update_fields=['estado'])

        messages.success(request, f"Estado del proyecto '{proyecto.nombre}' actualizado a: {proyecto.get_estado_display()}")
    else:
        messages.error(request, "Estado no válido.")

    return redirect('proyectos:proyecto_detail', pk=proyecto.id)


def actualizar_estado_tarea(request, pk):
    """
    Cambia el estado de la tarea y actualiza automáticamente el estado del proyecto asociado
    """
    tarea = get_object_or_404(Tarea, pk=pk)
    nuevo_estado = request.GET.get('estado_completado')

    # Validamos que el estado sea uno de los permitidos
    estados_validos = dict(Tarea.ESTADOS_COMPLETADO).keys()

    if nuevo_estado in estados_validos:
        tarea.estado_completado = nuevo_estado
        tarea.save(update_fields=['estado_completado'])

        proyecto = tarea.proyecto
        proyecto.actualizar_estado()  # Actualizamos el estado del proyecto basado en sus tareas

        messages.success(
            request,
            f"Estado de la tarea '{tarea.titulo}' actualizado a: {tarea.get_estado_completado_display()}"
        )
    else:
        messages.error(request, "Estado de tarea no válido.")

    return redirect('proyectos:tarea_detail', pk=tarea.id)


# =============================
# Vista de inicio (accesible para todos)
# =============================
def PaginaInicioView(request):
    """
    Vista para la página de inicio.
    Muestra un mensaje de bienvenida y opcionalmente una lista de proyectos.
    """
    proyectos = Proyecto.objects.all()[:5]  # Mostrar hasta 5 proyectos
    context = {
        'proyectos': proyectos,
        'titulo': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)


# =============================
# Vista para crear usuarios (solo Admin)
# =============================
@user_passes_test(es_admin, login_url='/')
def lista_usuarios(request):
    """
    Muestra la lista de todos los usuarios registrados.
    """
    usuarios = User.objects.all()
    return render(request, 'admin/lista_usuarios.html', {'usuarios': usuarios})


@user_passes_test(es_admin, login_url='/')
def crear_usuario(request):
    """
    Permite al Admin crear nuevos usuarios desde una vista personalizada.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, f'Usuario "{username}" creado exitosamente.')
                return redirect('proyectos:lista_usuarios')
        else:
            messages.error(request, 'Por favor, completa ambos campos.')

    return render(request, 'admin/crear_usuario.html')