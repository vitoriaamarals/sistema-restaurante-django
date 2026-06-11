from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Marmita, Pedido, ItemPedido
from .forms import CadastroForm

class ItemPedidoForm(forms.Form):
    TAMANHO_CHOICES = [
        ('P', 'Pequena'),
        ('G', 'Grande'),
    ]
    tamanho = forms.ChoiceField(
        choices=TAMANHO_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantidade = forms.IntegerField(
        min_value=1, 
        initial=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    observacao = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

class PedidoForm(forms.Form):
    endereco = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def lista_marmitas(request):
    marmitas = Marmita.objects.filter(disponivel=True)
    return render(request, 'core/marmitas.html', {'marmitas': marmitas})


@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, 'core/pedidos.html', {'pedidos': pedidos})


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'registration/cadastro.html', {'form': form})


@login_required
def criar_pedido(request, marmita_id):
    marmita = get_object_or_404(Marmita, id=marmita_id)

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST) # formulário correto sem endereço/telefone
        
        if form.is_valid():
            # 1. Buscamos ou criamos um pedido com status temporário 'CARRINHO'
            pedido, created = Pedido.objects.get_or_create(
                cliente=request.user,
                status='CARRINHO',
                defaults={
                    'endereco': 'A definir',
                    'telefone': 'A definir'
                }
            )

            # 2. Captura os dados limpos do formulário
            tamanho = form.cleaned_data['tamanho']
            quantidade = form.cleaned_data['quantidade']
            observacao = form.cleaned_data['observacao']

            # 3. Adiciona ou recupera o item associado a este carrinho
            item, item_created = ItemPedido.objects.get_or_create(
                pedido=pedido,
                marmita=marmita,
                tamanho=tamanho,
                defaults={
                    'quantidade': quantidade,
                    'observacao': observacao
                }
            )

            # Se o item já existia com o mesmo tamanho, apenas incrementa a quantidade
            if not item_created:
                item.quantidade += quantidade
                if observacao:
                    item.observacao = observacao
                item.save()

            pedido.save()

            # Redireciona o cliente para a listagem intermediária do Carrinho
            return redirect('carrinho')
    else:
        form = ItemPedidoForm()

    return render(request, 'core/criar_pedido.html', {'form': form, 'marmita': marmita})


@login_required
def ver_carrinho(request):
    # Busca o carrinho atual do usuário
    pedido = Pedido.objects.filter(cliente=request.user, status='CARRINHO').first()
    
    if pedido:
        # recalculo do valor do pedido
        total_calculado = sum(item.subtotal for item in pedido.itens.all())
        pedido.total = total_calculado
        pedido.save() # Atualiza o valor correto de forma definitiva no banco

    if request.method == 'POST' and pedido:
        # No Checkout, o cliente preenche os dados finais e fecha o carrinho
        pedido.endereco = request.POST.get('endereco')
        pedido.telefone = request.POST.get('telefone')

        pedido.forma_pagamento = request.POST.get('forma_pagamento')
        
        pedido.status = 'PREPARANDO' 
        pedido.save()
        return redirect('pedidos') # Redireciona para o histórico de pedidos

    return render(request, 'core/carrinho.html', {'pedido': pedido})