from django.core.management.base import BaseCommand
from proyecto_app.models import Proyecto
from django.contrib.auth.models import User
import random
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crea 60 proyectos nuevos, desde el 021 hasta el 080'

    def handle(self, *args, **kwargs):
        # Selecciona un usuario base para asignar los proyectos
        try:
            user = User.objects.get(username='testuser')  # ← Cambia esto si usas otro nombre
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("No se encontró el usuario 'testuser'. Asegúrate de tenerlo creado."))
            return

        # Fechas base
        fecha_inicio_base = timezone.now().date()
        estados = ['pdte', 'en_progreso', 'completado']

        nuevos_proyectos = []

        # Crea proyectos desde 021 hasta 080
        for i in range(21, 81):  # Incluye 021 a 080
            nombre = f'Proyecto {i:03d}'  # Formato con 3 dígitos (ej: Proyecto 021)
            descripcion = f'Descripción del Proyecto número {i:03d}'

            proyecto = Proyecto(
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio_base + timedelta(days=(i * 2)),  # Fechas progresivas
                fecha_fin=fecha_inicio_base + timedelta(days=(i * 5)),
                estado=random.choice(estados)
            )
            nuevos_proyectos.append(proyecto)

        # Guarda todos los proyectos en la base de datos
        Proyecto.objects.bulk_create(nuevos_proyectos)

        # Asigna los proyectos al usuario (opcional)
        proyectos_creados = Proyecto.objects.filter(nombre__startswith='Proyecto ')
        for proyecto in proyectos_creados:
            proyecto.usuarios.add(user)

        self.stdout.write(self.style.SUCCESS('✅ 60 proyectos creados y asignados correctamente.'))