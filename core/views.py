from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Marmita, Pedido, ItemPedido
from django.shortcuts import render, redirect
from .forms import CadastroForm, PedidoForm
from django import forms


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def lista_marmitas(request):
    marmitas = Marmita.objects.filter(disponivel=True)

    return render(
        request,
        'core/marmitas.html',
        {'marmitas': marmitas}
    )


@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(
        cliente=request.user
    )

    return render(
        request,
        'core/pedidos.html',
        {'pedidos': pedidos}
    )

def cadastro(request):

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CadastroForm()

    return render(
        request,
        'registration/cadastro.html',
        {'form': form}
    )

class PedidoForm(forms.Form):

    TAMANHO_CHOICES = [
        ('P', 'Pequena'),
        ('G', 'Grande'),
    ]

    tamanho = forms.ChoiceField(
        choices=TAMANHO_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    endereco = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    telefone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3
            }
        )
    )

@login_required
def criar_pedido(request, marmita_id):

    marmita = Marmita.objects.get(id=marmita_id)

    if request.method == 'POST':

        form = PedidoForm(request.POST)

        if form.is_valid():

            pedido = Pedido.objects.create(
                cliente=request.user,
                endereco=form.cleaned_data['endereco'],
                telefone=form.cleaned_data['telefone']
            )

            ItemPedido.objects.create(
                pedido=pedido,
                marmita=marmita,
                tamanho=form.cleaned_data['tamanho'],
                quantidade=form.cleaned_data['quantidade'],
                observacao=form.cleaned_data['observacao']
            )

            return redirect('pedidos')

    else:
        form = PedidoForm()

    return render(
        request,
        'core/criar_pedido.html',
        {
            'form': form,
            'marmita': marmita
        }
    )