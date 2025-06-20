from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ContaReceber
from .forms import ContaReceberForm
from .models import ContaPagar
from .forms import ContaPagarForm
from datetime import date
from django.db.models import Q
from datetime import date

@login_required
def lista_contas_receber(request):
    contas = ContaReceber.objects.select_related('cliente').all()

    cliente_nome = request.GET.get('cliente', '')
    status = request.GET.get('status', '')

    if cliente_nome:
        contas = contas.filter(cliente__nome__icontains=cliente_nome)

    if status == 'pago':
        contas = contas.filter(pago=True)
    elif status == 'aberto':
        contas = contas.filter(pago=False, data_vencimento__gte=date.today())
    elif status == 'vencido':
        contas = contas.filter(pago=False, data_vencimento__lt=date.today())

    contas = contas.order_by('-data_vencimento')
    return render(request, 'financeiro/contas_receber.html', {'contas': contas, 'today': date.today()})


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

@login_required
def editar_conta_receber(request, conta_id):
    conta = get_object_or_404(ContaReceber, id=conta_id)
    if request.method == 'POST':
        form = ContaReceberForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            return redirect('lista_contas_receber')
    else:
        form = ContaReceberForm(instance=conta)
    return render(request, 'financeiro/form_receber.html', {'form': form})

@login_required
def excluir_conta_receber(request, conta_id):
    conta = get_object_or_404(ContaReceber, id=conta_id)
    if request.method == 'POST':
        conta.delete()
        return redirect('lista_contas_receber')
    return render(request, 'financeiro/confirma_exclusao.html', {'conta': conta})

@login_required
def editar_conta_pagar(request, conta_id):
    conta = get_object_or_404(ContaPagar, id=conta_id)
    if request.method == 'POST':
        form = ContaPagarForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            return redirect('lista_contas_pagar')
    else:
        form = ContaPagarForm(instance=conta)
    return render(request, 'financeiro/form_pagar.html', {'form': form})

@login_required
def excluir_conta_pagar(request, conta_id):
    conta = get_object_or_404(ContaPagar, id=conta_id)
    if request.method == 'POST':
        conta.delete()
        return redirect('lista_contas_pagar')
    return render(request, 'financeiro/confirma_exclusao.html', {'conta': conta})

@login_required
def lista_contas_pagar(request):
    contas = ContaPagar.objects.all()

    fornecedor = request.GET.get('fornecedor', '')
    status = request.GET.get('status', '')

    if fornecedor:
        contas = contas.filter(fornecedor__icontains=fornecedor)

    if status == 'pago':
        contas = contas.filter(pago=True)
    elif status == 'aberto':
        contas = contas.filter(pago=False, data_vencimento__gte=date.today())
    elif status == 'vencido':
        contas = contas.filter(pago=False, data_vencimento__lt=date.today())

    contas = contas.order_by('-data_vencimento')
    return render(request, 'financeiro/contas_pagar.html', {
        'contas': contas,
        'today': date.today()
    })
