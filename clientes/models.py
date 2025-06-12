from django.db import models

class Cliente(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('prospect', 'Prospect'),
    ]

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='prospect')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Interacao(models.Model):
    TIPO_CHOICES = [
        ('email', 'E-mail'),
        ('chamada', 'Chamada'),
        ('whatsapp', 'WhatsApp'),
        ('outro', 'Outro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='interacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    data_interacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.tipo}\""
    
class Interacao(models.Model):
    TIPO_CHOICES = [
        ('email', 'E-mail'),
        ('chamada', 'Chamada'),
        ('whatsapp', 'WhatsApp'),
        ('outro', 'Outro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='interacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    data_interacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.tipo}"

