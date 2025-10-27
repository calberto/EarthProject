from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Continentes, Patrias, Estados, Cidades

class ContinenteForm(forms.ModelForm):
    class Meta:
        model = Continentes
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
        fields = ['nome', 'uf', 'versao', 'patrias', 'flag', 'created_at']  # Apenas campos editáveis

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

class CidadeFormOld(forms.ModelForm):
    class Meta:
        model = Cidades
        fields = ['nome', 'estados']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da cidade',
                'required': True
            }),
            'estados': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }
        labels = {
            'nome': 'Nome da Cidade',
            'estados': 'Estado'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Popula o select com todos os estados ordenados por nome
        self.fields['estados'].queryset = Estados.objects.all().order_by('nome')
        self.fields['estados'].empty_label = "Selecione um estado"


class NewContinenteForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}))
    versao = forms.IntegerField(label="Versão", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Versão'}))
	
	  