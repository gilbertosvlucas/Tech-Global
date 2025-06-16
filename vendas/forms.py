from django import forms
from .models import Orcamento, ItemOrcamento
from django.forms import inlineformset_factory

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['cliente', 'status', 'observacoes']


class ItemOrcamentoForm(forms.ModelForm):
    class Meta:
        model = ItemOrcamento
        fields = ['produto', 'quantidade', 'preco_unitario']


# Formset para múltiplos itens no orçamento
ItemOrcamentoFormSet = inlineformset_factory(
    Orcamento,
    ItemOrcamento,
    form=ItemOrcamentoForm,
    extra=1,
    can_delete=True
)
