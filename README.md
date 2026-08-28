# LoveStock Cake

Sistema de gerenciamento de estoque, receitas e produção para confeitaria, desenvolvido em Python no terminal utilizando interface interativa com navegação por setas e visual moderno com Rich.

---

## Sobre o projeto

O LoveStock Cake foi criado para facilitar o controle de ingredientes e receitas de uma confeitaria de forma simples, rápida e organizada.

O sistema permite:

- Gerenciar estoque de ingredientes
- Criar e editar receitas
- Produzir receitas automaticamente descontando ingredientes do estoque
- Navegar por menus interativos usando teclado
- Armazenar dados em arquivos JSON

---

## Tecnologias utilizadas

- Python 3
- JSON
- Rich
- Winsound
- Msvcrt

---

## Estrutura do projeto

```bash
LoveStock-Cake/
│
├── estoque.json
├── receita.json
├── main.py
└── README.md
```

---

## Funcionalidades

### Controle de Estoque

- Adicionar ingredientes
- Remover ingredientes
- Reduzir quantidade específica
- Visualizar estoque completo

---

### Sistema de Receitas

- Criar receitas
- Remover receitas
- Editar ingredientes
- Visualizar receitas cadastradas

---

### Produção

Ao produzir uma receita:

- O sistema verifica automaticamente se há ingredientes suficientes
- Os ingredientes são descontados do estoque
- Exibe mensagens de erro caso falte algum item

---

## Navegação

O sistema utiliza:

| Tecla | Função |
|---|---|
| ↑ | Subir opção |
| ↓ | Descer opção |
| Enter | Selecionar |

---

## Sons do sistema

O programa possui feedback sonoro para melhorar a experiência:

- Som de confirmação
- Som de erro
- Som de navegação

---

## Instalação

### 1. Baixe os arquivos do projeto

Coloque os arquivos abaixo na mesma pasta:

```bash
main.py
estoque.json
receita.json
```

---

### 2. Instale as dependências

```bash
pip install rich
```

---

## Executando o projeto

```bash
python main.py
```

---

## Armazenamento de dados

Os dados são armazenados automaticamente em arquivos JSON.

### estoque.json

```json
{
    "farinha": 5000,
    "açucar": 4000,
    "ovos": 100,
    "leite": 3000,
    "fermento": 200,
    "chocolate": 1500,
    "manteiga": 500
}
```

### receita.json

```json
{
  "bolo_simples": {
    "farinha": 200,
    "açucar": 150,
    "ovos": 3,
    "leite": 200,
    "fermento": 10
  },

  "bolo_chocolate": {
    "farinha": 200,
    "aucar": 150,
    "ovos": 3,
    "leite": 200,
    "chocolate": 100,
    "fermento": 10
  },

  "brigadeiro": {
    "leite": 200,
    "chocolate": 150,
    "manteiga": 20
  }
}
```

---

## Tratamento de erros

O sistema possui tratamento para:

- JSON inválido
- Valores numéricos incorretos
- Arquivos inexistentes
- Erros inesperados

---

## Interface

O projeto utiliza a biblioteca Rich para:

- Painéis estilizados
- Tabelas organizadas
- Cores no terminal
- Interface mais moderna

---

## Exemplos Visuais

Abaixo estão alguns exemplos da interface e das principais funcionalidades do LoveStock Cake.

### Menu Principal

<p align="center">
![Menu principal](./imagens/confeitaria0.png)
</p>

O menu principal permite acessar as funcionalidades de controle de estoque, receitas e produção de forma simples e intuitiva.

---

### Controle de Estoque

<p align="center">
![Menu principal](./imagens/confeitaria1.png)
</p>

Nesta tela, o usuário pode visualizar e gerenciar os ingredientes disponíveis, adicionando, removendo ou alterando suas quantidades.

---

### Sistema de Receitas

<p align="center">
  ![Menu principal](./imagens/confeitaria2.png)
</p>

O sistema permite cadastrar, editar, remover e visualizar receitas, juntamente com os ingredientes necessários para cada produção.

---

### Produção de Receitas

<p align="center">
  ![Menu principal](./imagens/confeitaria3.png)
</p>

Ao selecionar uma receita e informar a quantidade desejada, o sistema verifica automaticamente a disponibilidade dos ingredientes e realiza o desconto no estoque.

---

## Requisitos

- Windows
- Python 3.10+
- Terminal compatível

> O projeto utiliza `winsound` e `msvcrt`, bibliotecas nativas do Windows.

---

## Melhorias futuras

- Sistema de login
- Histórico de produção
- Relatórios
- Interface gráfica
- Backup automático
- Cadastro de preços
- Controle de validade

---

## Autor

Desenvolvido por Lionel Gonçalves Dantas e Daniel de jesus.

---

## Licença

Este projeto é livre para estudos e uso pessoal.
