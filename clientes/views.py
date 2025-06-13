from django.shortcuts import render, redirect
from .models import Cliente
from financeiro.models import ContaReceber
from .forms import ClienteForm
from .forms import ClienteForm, InteracaoForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form})

@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/confirma_exclusao.html', {'cliente': cliente})

@login_required
def listar_interacoes(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    interacoes = cliente.interacoes.all().order_by('-data_interacao')
    return render(request, 'clientes/interacoes.html', {
        'cliente': cliente,
        'interacoes': interacoes
    })

@login_required
def nova_interacao(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = InteracaoForm(request.POST)
        if form.is_valid():
            interacao = form.save(commit=False)
            interacao.cliente = cliente
            interacao.save()
            return redirect('listar_interacoes', cliente_id=cliente.id)
    else:
        form = InteracaoForm()
    return render(request, 'clientes/nova_interacao.html', {
        'form': form,
        'cliente': cliente
    })


