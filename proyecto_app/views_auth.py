# proyecto_app/views_auth.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages  # Muestra mensajes bonitos de éxito o error
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Mensaje de éxito al registrar
            messages.success(
                request,
                f'¡Bienvenido, {user.username}! Te has registrado exitosamente.'
            )
            return redirect('home')
        else:
            # Mensaje de error si hay campos inválidos
            messages.error(
                request,
                'Hubo errores en el formulario. Por favor corrige los campos.'
            )

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})