from django import forms
from .models import Continente, Patrias, Estados, Cidades

class ContinenteForm(forms.ModelForm):
    class Meta:
        model = Continente
        fields = '__all__'

class PatriaForm(forms.ModelForm):
    class Meta:
        model = Patrias
        fields = '__all__'

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estados
        fields = '__all__'

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidades
        fields = '__all__'