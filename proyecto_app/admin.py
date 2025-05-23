from django.contrib import admin
from .models import Proyecto, Tarea


# Configuración del Admin para Proyecto
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_inicio', 'fecha_fin')
    list_filter = ('estado', 'usuarios')
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('usuarios',)  # Mejor interfaz para ManyToManyField
    ordering = ('nombre',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Usuarios Asignados', {
            'fields': ('usuarios',)
        }),
    )


# Si también quieres ver Tarea en Admin
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'usuario', 'estado_completado')
    list_filter = ('estado_completado', 'proyecto')
    search_fields = ('titulo',)
    autocomplete_fields = ['proyecto', 'usuario']
    ordering = ('titulo',)