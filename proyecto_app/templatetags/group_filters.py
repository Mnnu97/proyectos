from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Uso en plantilla:
    {% if user|has_group:"Admin" %}
        <p>Contenido para admins</p>
    {% endif %}
    """
    return user.groups.filter(name=group_name).exists()
