from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from financeiro.models import ContaReceber, ContaPagar
from clientes.models import Cliente

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
