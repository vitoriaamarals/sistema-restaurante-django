from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):

    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })

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