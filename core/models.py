from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


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

    preco_pequena = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    preco_grande = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    categoria = models.ForeignKey(
        CategoriaMarmita,
        on_delete=models.CASCADE
    )

    disponivel = models.BooleanField(default=True)

    refrigerante = models.BooleanField(default=False, verbose_name="Inclui Refrigerante?")
    
    def clean(self):

        if self.preco_pequena <= 0:
            raise ValidationError(
                "O preço da marmita pequena deve ser maior que zero."
            )

        if self.preco_grande <= 0:
            raise ValidationError(
                "O preço da marmita grande deve ser maior que zero."
            )

    def __str__(self):
        return self.nome


class Pedido(models.Model):

    STATUS_CHOICES = [
        ('CARRINHO', 'Carrinho'),
        ('PREPARANDO', 'Preparando'),
        ('SAIU_ENTREGA', 'Saiu para entrega'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    data = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='CARRINHO'
    )

    endereco = models.CharField(max_length=255)

    telefone = models.CharField(max_length=20)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"
    
    def atualizar_total(self):
        total = sum(item.subtotal for item in self.itens.all())
        self.total = total
        self.save(update_fields=['total'])

class ItemPedido(models.Model):

    TAMANHO_CHOICES = [
        ('P', 'Pequena'),
        ('G', 'Grande'),
    ]

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    marmita = models.ForeignKey(
        Marmita,
        on_delete=models.CASCADE
    )

    tamanho = models.CharField(
        max_length=1,
        choices=TAMANHO_CHOICES
    )

    quantidade = models.PositiveIntegerField()

    observacao = models.TextField(
        blank=True,
        null=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def clean(self):

        if self.quantidade <= 0:
            raise ValidationError(
                "A quantidade deve ser maior que zero."
            )

    def __str__(self):
        return f"{self.quantidade}x {self.marmita.nome}"
    

    def save(self, *args, **kwargs):

        if self.tamanho == 'P':
            preco = self.marmita.preco_pequena
        else:
            preco = self.marmita.preco_grande

        self.subtotal = Decimal(preco) * self.quantidade

        super().save(*args, **kwargs)

        if self.pedido_id:
            self.pedido.atualizar_total()
