from django import forms
from financeiro.models import ContaReceber
from .models import ContaPagar


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = '__all__'

class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = '__all__'