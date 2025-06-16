from django.db import models

class Produto(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return self.nome

from clientes.models import Cliente

class Orcamento(models.Model):
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome}"

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


class ItemOrcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} (x{self.quantidade})"

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"
