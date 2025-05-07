import os
import django

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyectos.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    print("Resultado de prueba:", result)
