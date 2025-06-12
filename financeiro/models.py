from django.db import models
from clientes.models import Cliente

class ContaReceber(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente.nome} - {self.descricao}"

class ContaPagar(models.Model):
    fornecedor = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fornecedor} - {self.descricao}"
