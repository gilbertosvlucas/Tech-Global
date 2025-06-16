from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from financeiro.models import ContaReceber, ContaPagar
from clientes.models import Cliente
from django.db.models import Sum, Q
from datetime import date
from financeiro.models import ContaReceber, ContaPagar
from clientes.models import Cliente
from django.utils.safestring import mark_safe
import json

@login_required
def dashboard(request):
    total_receber = ContaReceber.objects.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    total_pagar = ContaPagar.objects.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receber - total_pagar
    clientes_ativos = Cliente.objects.count()
    vencidas_hoje = ContaReceber.objects.filter(pago=False, data_vencimento=date.today()).count()

    return render(request, 'dashboard.html', {
        'total_receber': total_receber,
        'total_pagar': total_pagar,
        'saldo': saldo,
        'clientes_ativos': clientes_ativos,
        'vencidas_hoje': vencidas_hoje
    })

@login_required
def dashboard(request):
    total_receber = ContaReceber.objects.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    total_pagar = ContaPagar.objects.filter(pago=False).aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receber - total_pagar

    clientes_ativos = Cliente.objects.count()
    vencidas_hoje = ContaReceber.objects.filter(pago=False, data_vencimento=date.today()).count()

    # Dados para o gráfico de contas a receber
    pago_receber = ContaReceber.objects.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    em_aberto_receber = ContaReceber.objects.filter(pago=False, data_vencimento__gte=date.today()).aggregate(Sum('valor'))['valor__sum'] or 0
    vencido_receber = ContaReceber.objects.filter(pago=False, data_vencimento__lt=date.today()).aggregate(Sum('valor'))['valor__sum'] or 0

    # Dados para o gráfico de contas a pagar
    pago_pagar = ContaPagar.objects.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    em_aberto_pagar = ContaPagar.objects.filter(pago=False, data_vencimento__gte=date.today()).aggregate(Sum('valor'))['valor__sum'] or 0
    vencido_pagar = ContaPagar.objects.filter(pago=False, data_vencimento__lt=date.today()).aggregate(Sum('valor'))['valor__sum'] or 0

    return render(request, 'dashboard.html', {
        'total_receber': total_receber,
        'total_pagar': total_pagar,
        'saldo': saldo,
        'clientes_ativos': clientes_ativos,
        'vencidas_hoje': vencidas_hoje,
        'pago_receber': pago_receber,
        'em_aberto_receber': em_aberto_receber,
        'vencido_receber': vencido_receber,
        'pago_pagar': pago_pagar,
        'em_aberto_pagar': em_aberto_pagar,
        'vencido_pagar': vencido_pagar,

        'dados_graficos': mark_safe(json.dumps({
    'receber': {
        'pago': float(pago_receber or 0),
        'aberto': float(em_aberto_receber or 0),
        'vencido': float(vencido_receber or 0),
    },
    'pagar': {
        'pago': float(pago_pagar or 0),
        'aberto': float(em_aberto_pagar or 0),
        'vencido': float(vencido_pagar or 0),
    }
}))
    })
