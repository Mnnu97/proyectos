from django.test import TestCase
from django.urls import reverse
from .models import Proyecto, Tarea

class ProyectoTests(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto de ejemplo',
            descripcion='Este es un proyecto de ejemplo.',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-12-31'
        )

    def test_proyecto_creation(self):
        self.assertTrue(isinstance(self.proyecto, Proyecto))
        self.assertEqual(self.proyecto.__str__(), 'Proyecto de ejemplo')

    def test_proyecto_list_view(self):
        response = self.client.get(reverse('proyecto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proyecto de ejemplo')

    def test_proyecto_detail_view(self):
        response = self.client.get(reverse('proyecto_detail', args=[self.proyecto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proyecto de ejemplo')
