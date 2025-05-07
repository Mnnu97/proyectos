from django import forms
from .models import Proyecto, Tarea

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_fin': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%d']


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'estado_completado', 'proyecto']
        widgets = {
            'fecha_vencimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'estado_completado': forms.Select(attrs={'class': 'form-select'}),
            'proyecto': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer formato inicial en campo de fecha
        if 'fecha_vencimiento' in self.fields:
            self.fields['fecha_vencimiento'].input_formats = ['%Y-%m-%d']