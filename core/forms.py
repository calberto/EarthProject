from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Continente, Patrias, Estados, Cidades

class ContinenteForm(forms.ModelForm):
    class Meta:
        model = Continente
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))    

class PatriaForm(forms.ModelForm):
    class Meta:
        model = Patrias
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))    

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estados
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))    

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidades
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))    
    