from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Proyecto

class ProyectoTests(TestCase):
    def setUp(self):
        # Crear un usuario común
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Crear un proyecto y asignarlo al usuario
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto de ejemplo',
            descripcion='Este es un proyecto de ejemplo.',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-12-31',
            estado='pdte'
        )
        self.proyecto.usuarios.add(self.user)  

    def test_proyecto_creation(self):
        self.assertTrue(isinstance(self.proyecto, Proyecto))
        self.assertEqual(self.proyecto.nombre, 'Proyecto de ejemplo')
        self.assertEqual(str(self.proyecto), 'Proyecto de ejemplo')

    def test_proyecto_list_view(self):
        response = self.client.get(reverse('proyectos:proyecto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyecto_app/proyecto_list.html')
        self.assertContains(response, 'Proyecto de ejemplo')  

    def test_proyecto_detail_view(self):
        response = self.client.get(reverse('proyectos:proyecto_detail', args=[self.proyecto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyecto_app/proyecto_detail.html')
        self.assertContains(response, 'Proyecto de ejemplo') 