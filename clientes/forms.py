from django import forms
from .models import Cliente
from .models import Interacao

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['tipo', 'descricao']