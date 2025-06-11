# proyecto_app/views_import.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Proyecto
from django.contrib import messages


def es_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser


@user_passes_test(es_admin, login_url='/')
def importar_proyectos(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        try:
            df = pd.read_excel(archivo)

            for _, row in df.iterrows():
                Proyecto.objects.create(
                    nombre=row['nombre'],
                    descripcion=row.get('descripcion', ''),
                    fecha_inicio=row.get('fecha_inicio'),
                    fecha_fin=row.get('fecha_fin'),
                    estado=row.get('estado', 'pdte')
                )

            messages.success(request, "✅ Proyectos importados correctamente.")
        except Exception as e:
            messages.error(request, f"❌ Error al importar: {e}")

        return redirect(reverse_lazy('proyectos:inicio'))

    return render(request, 'admin/importar_datos.html')