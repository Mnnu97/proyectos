# proyecto_app/views_usuarios.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Proyecto


def es_admin(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(es_admin, login_url='/')
def lista_usuarios(request):
    """
    Muestra la lista de todos los usuarios del sistema.
    - Los usuarios Admin aparecen primero
    - Los usuarios normales después
    - Solo accesible por usuarios del grupo 'Admin'
    """
    admin_users = User.objects.filter(groups__name='Admin')
    other_users = User.objects.exclude(groups__name='Admin')

    usuarios = list(admin_users) + list(other_users)

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
                nuevo_usuario = User.objects.create_user(username=username, password=password)
                messages.success(request, f'Usuario "{username}" creado exitosamente.')
                return redirect('proyectos:lista_usuarios')
        else:
            messages.error(request, 'Por favor, completa ambos campos.')

    return render(request, 'admin/crear_usuario.html')


@user_passes_test(es_admin, login_url='/')
def eliminar_usuario(request, pk):
    """
    Permite al Admin eliminar un usuario existente.
    No permite eliminarse a sí mismo.
    """
    usuario = get_object_or_404(User, pk=pk)

    if usuario == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('proyectos:lista_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'Usuario "{usuario.username}" eliminado correctamente.')
        return redirect('proyectos:lista_usuarios')

    return render(request, 'admin/eliminar_usuario.html', {'usuario': usuario})


@user_passes_test(es_admin, login_url='/')
def asignar_proyectos(request, pk):
    """
    Permite al Admin asignar uno o varios proyectos a un usuario.
    No se puede asignar proyectos a otro Admin.
    """
    usuario = get_object_or_404(User, pk=pk)

    if usuario.groups.filter(name='Admin').exists():
        messages.warning(request, 'No puedes asignar proyectos a un administrador.')
        return redirect('proyectos:lista_usuarios')

    proyectos = Proyecto.objects.all()

    if request.method == 'POST':
        selected_proyectos = request.POST.getlist('proyectos')  # Obtiene lista de IDs seleccionados
        usuario.proyectos_usuario.set(selected_proyectos)  # Asigna los proyectos al usuario
        messages.success(request, f'Proyectos asignados al usuario "{usuario.username}"')
        return redirect('proyectos:lista_usuarios')

    return render(request, 'admin/asignar_proyectos.html', {
        'usuario': usuario,
        'proyectos': proyectos,
        'proyectos_usuario': usuario.proyectos_usuario.all()
    })


@user_passes_test(es_admin, login_url='/')
def ver_proyectos_usuario(request, pk):
    """
    Muestra los proyectos asignados a un usuario específico.
    Solo accesible por usuarios Admin.
    """
    usuario = get_object_or_404(User, pk=pk)
    
    return render(request, 'admin/ver_proyectos_usuario.html', {
        'usuario': usuario,
        'proyectos_asignados': usuario.proyectos_usuario.all()
    })


@user_passes_test(es_admin, login_url='/')
def detalle_usuario(request, pk):
    """
    Muestra información detallada de un usuario:
    - Sus proyectos asignados
    """
    usuario = get_object_or_404(User, pk=pk)

    context = {
        'usuario': usuario,
        'proyectos_asignados': usuario.proyectos_usuario.all(),
    }

    return render(request, 'admin/detalle_usuario.html', context)