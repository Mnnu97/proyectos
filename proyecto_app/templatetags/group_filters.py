# proyecto_app/templatetags/group_filters.py

from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Filtro personalizado para verificar si un usuario pertenece a un grupo específico.
    
    Uso en plantilla:
    {% if user|has_group:"Admin" %}
        <p>Contenido solo para administradores</p>
    {% endif %}
    """
    if not user.is_authenticated:
        return False
    
    return user.groups.filter(name=group_name).exists()