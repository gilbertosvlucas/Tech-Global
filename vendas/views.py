from django.shortcuts import render, redirect, get_object_or_404
from .models import Orcamento
from .forms import OrcamentoForm, ItemOrcamentoFormSet
from django.contrib.auth.decorators import login_required
from financeiro.models import ContaReceber
from datetime import date
from .models import Pedido, ItemPedido, Orcamento

@login_required
def novo_orcamento(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        formset = ItemOrcamentoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            orcamento = form.save()
            formset.instance = orcamento
            formset.save()
            return redirect('lista_orcamentos')
    else:
        form = OrcamentoForm()
        formset = ItemOrcamentoFormSet()

    return render(request, 'vendas/novo_orcamento.html', {
        'form': form,
        'formset': formset,
        'editando': False  # ← Aqui indicamos que está criando
    })


@login_required
def lista_orcamentos(request):
    orcamentos = Orcamento.objects.select_related('cliente').all().order_by('-data')
    return render(request, 'vendas/lista_orcamentos.html', {'orcamentos': orcamentos})

@login_required
def editar_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        formset = ItemOrcamentoFormSet(request.POST, instance=orcamento)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('lista_orcamentos')
    else:
        form = OrcamentoForm(instance=orcamento)
        formset = ItemOrcamentoFormSet(instance=orcamento)

    return render(request, 'vendas/novo_orcamento.html', {
        'form': form,
        'formset': formset,
        'editando': True
    })

@login_required
def excluir_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    if request.method == 'POST':
        orcamento.delete()
        return redirect('lista_orcamentos')
    return render(request, 'vendas/confirma_exclusao.html', {'orcamento': orcamento})


@login_required
def editar_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    status_anterior = orcamento.status  # 👈 salva o status antes da edição

    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        formset = ItemOrcamentoFormSet(request.POST, instance=orcamento)

        if form.is_valid() and formset.is_valid():
            orcamento = form.save()
            formset.save()

            # ✅ Gera conta a receber se aprovado agora e ainda não havia sido aprovado antes
            if orcamento.status == 'aprovado' and status_anterior != 'aprovado':
                ContaReceber.objects.create(
                    cliente=orcamento.cliente,
                    descricao=f'Orçamento #{orcamento.id} aprovado',
                    valor=orcamento.total(),
                    data_vencimento=date.today()  # você pode deixar fixo ou pedir ao usuário
                )

            return redirect('lista_orcamentos')
    else:
        form = OrcamentoForm(instance=orcamento)
        formset = ItemOrcamentoFormSet(instance=orcamento)

    return render(request, 'vendas/novo_orcamento.html', {
        'form': form,
        'formset': formset,
        'editando': True
    })

@login_required
def gerar_pedido(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)

    if orcamento.status != 'aprovado':
        return redirect('lista_orcamentos')  # segurança: só gera de aprovados

    # Cria o pedido
    pedido = Pedido.objects.create(
        cliente=orcamento.cliente,
        observacoes=orcamento.observacoes
    )

    # Copia os itens
    for item in orcamento.itens.all():
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        )

    return redirect('lista_pedidos')

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').prefetch_related('itens').order_by('-data_pedido')
    return render(request, 'vendas/lista_pedidos.html', {'pedidos': pedidos})
