# 🍱 Sistema de Delivery de Marmitas

Projeto desenvolvido para a disciplina **GAC116 - Programação Web** utilizando o framework Django.

A aplicação simula um sistema de delivery de marmitas, permitindo o gerenciamento de categorias, produtos e pedidos através de um ambiente administrativo autenticado, além de oferecer uma interface para que os clientes visualizem o cardápio, realizem seu cadastro e gerenciem seus próprios pedidos.

---

## 👥 Integrantes

* Maria Eduarda Ferreira da Silva
* Vitória Christie Amaral Santos
* Vinicius Passos Oliveira

---

## 🚀 Funcionalidades Implementadas

### 👤 Área do Cliente
* **Autenticação Completa:** Cadastro de novos usuários, Login e Logout protegidos.
* **Cardápio Interativo:** Visualização de marmitas disponíveis.
* **Fluxo de Pedidos:** Tela para montagem do pedido com quantidade, endereço de entrega, telefone e campo para observações.
* **Histórico de Pedidos:** Área para o cliente acompanhar suas solicitações anteriores.

### 🛠️ Área Administrativa
* **Interface Customizada:** Ambiente administrativo gerenciado através do pacote *Jazzmin*.
* **Gestão de Cardápio:** Cadastro, edição e exclusão de categorias e marmitas.
* **Painel de Controle de Pedidos:** Visualização centralizada das vendas e alteração de status (Carrinho, Preparando, Saiu para Entrega, Entregue, Cancelado).

### ⚙️ Lógica de Negócio (Backend)
* **Persistência de Dados:** Uso de banco de dados relacional.
* **Cálculo Automático:** Processamento em tempo real do subtotal de cada item (Preço × Quantidade) e do valor total acumulado do pedido.

---

## 🗂️ Modelagem

O sistema possui as seguintes entidades:

* CategoriaMarmita
* Marmita
* Pedido
* ItemPedido
* User (Django)

### Relacionamentos
![Diagrama de Relacionamentos](assets/diagrama-django.jpeg)

---

## 💻 Tecnologias Utilizadas

* Python 3
* Django 6
* SQLite3
* Jazzmin
* Git/GitHub

---

## ⚙️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/vitoriaamarals/sistema-restaurante-django
```

### 2. Entrar na pasta do projeto

```bash
cd sistema-restaurante-django
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows (Prompt de Comando):

```bash
.\venv\Scripts\activate
```
Linux / macOS (e Git Bash no Windows):

```bash
source venv/bin/activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

### 6. Aplicar migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 7. Criar superusuário

```bash
python manage.py createsuperuser
```

### 8. Executar servidor

```bash
python manage.py runserver
```

---

## 🔐 Acesso ao Sistema

### Página inicial

```text
http://127.0.0.1:8000/
```

### Painel administrativo

```text
http://127.0.0.1:8000/admin
```

---

## 📁 Estrutura do Projeto

```text
sistema-restaurante-django/
├── assets/
├── core/
│   ├── migrations/
│   ├── admin.py
│   └── models.py
├── restaurante/
│   └── settings.py
├── templates/
│   ├── core/
│   └── registration/
├── manage.py
|── README.md
└── requirements.txt
```

---
