from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ContaReceber
from .forms import ContaReceberForm
from .models import ContaPagar
from .forms import ContaPagarForm

@login_required
def lista_contas_receber(request):
    contas = ContaReceber.objects.all().order_by('-data_vencimento')
    return render(request, 'financeiro/contas_receber.html', {'contas': contas})

@login_required
def nova_conta_receber(request):
    if request.method == 'POST':
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contas_receber')
    else:
        form = ContaReceberForm()
    return render(request, 'financeiro/form_receber.html', {'form': form})

@login_required
def lista_contas_pagar(request):
    contas = ContaPagar.objects.all().order_by('-data_vencimento')
    return render(request, 'financeiro/contas_pagar.html', {'contas': contas})

@login_required
def nova_conta_pagar(request):
    if request.method == 'POST':
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contas_pagar')
    else:
        form = ContaPagarForm()
    return render(request, 'financeiro/form_pagar.html', {'form': form})
