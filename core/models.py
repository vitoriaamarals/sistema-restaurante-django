from django.db import models
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome


class CategoriaMarmita(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Marmita(models.Model):

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(CategoriaMarmita, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)

    def clean(self):
        if self.preco <= 0:
            raise ValidationError("O preço deve ser maior que zero.")

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PREPARANDO', 'Preparando'),
        ('ENTREGUE', 'Entregue'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"


class ItemPedido(models.Model):
    TAMANHO_CHOICES = [
        ('P', 'Pequena'),
        ('M', 'Média'),
        ('G', 'Grande'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    marmita = models.ForeignKey(Marmita, on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=1, choices=TAMANHO_CHOICES)
    quantidade = models.PositiveIntegerField()
    observacao = models.TextField(blank=True, null=True)

    def clean(self):
        if self.quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero.")

    def __str__(self):
        return f"{self.quantidade}x {self.marmita.nome}"

        