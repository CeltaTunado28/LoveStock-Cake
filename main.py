import time
import winsound
import json
import os
import msvcrt

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_RECEITAS = "receita.json"


def beep(tipo='ok'):

    if tipo == 'ok':
        winsound.Beep(1000, 100)
        winsound.Beep(1300, 150)
        winsound.Beep(900, 100)

    elif tipo == 'deu ruim':
        winsound.Beep(700, 100)
        time.sleep(0.05)
        winsound.Beep(500, 120)
        time.sleep(0.05)
        winsound.Beep(300, 180)

    elif tipo == 'click':
        winsound.Beep(1000, 30)
        time.sleep(0.01)
        winsound.Beep(800, 20)


def menu_setas(opcoes, titulo=''):
    atual = 0

    while True:
        os.system('cls')

        linhas = []

        for i, opcao in enumerate(opcoes):

            if i == atual:
                linhas.append(f'[#ff69b4] ❤️   {opcao}[/]')
            else:
                linhas.append(f' {opcao}')

        console.print(
            Panel(
                '\n'.join(linhas),
                title=titulo,
                style="#e7b7cf"
            )
        )

        tecla = msvcrt.getch()

        if tecla == b'\xe0':
            tecla = msvcrt.getch()

            if tecla == b'H':
                atual -= 1
                beep('click')

            elif tecla == b'P':
                atual += 1
                beep('click')

        elif tecla == b'\r':
            beep('ok')
            return atual

        atual %= len(opcoes)


def carregar_json(nome_arquivo):

    try:

        if not os.path.exists(nome_arquivo):
            return {}

        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        beep('deu ruim')
        console.print(f'[red]JSON inválido em {nome_arquivo}[/red]')
        return {}

    except Exception as e:
        beep('deu ruim')
        console.print(f'[red]Erro ao carregar: {e}[/red]')
        return {}


def salvar_json(nome_arquivo, dados):

    with open(nome_arquivo, "w", encoding='utf-8') as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    beep('ok')


def input_float(mensagem):

    while True:

        try:
            valor = Prompt.ask(mensagem)
            numero = float(valor.replace(",", "."))

            if numero <= 0:
                beep('deu ruim')
                console.print('[red]Digite um número maior que zero[/red]')
                continue

            return numero

        except:
            beep('deu ruim')
            console.print('[red]Número inválido[/red]')


def mostrar_estoque(estoque):

    tabela = Table(title='Estoque')

    tabela.add_column('Ingrediente')
    tabela.add_column('Quantidade')

    if not estoque:
        console.print('[yellow]Estoque vazio[/yellow]')
        return

    for ingrediente, quantidade in estoque.items():
        tabela.add_row(ingrediente, str(quantidade))

    console.print(tabela)


def menu_estoque():

    while True:

        estoque = carregar_json(ARQUIVO_ESTOQUE)

        opcao = menu_setas(
            [
                'Adicionar',
                'Remover total',
                'Remover quantidade',
                'Ver estoque',
                'Voltar'
            ],
            'ESTOQUE'
        )

        if opcao == 0:

            nome = Prompt.ask('Ingrediente').strip().lower()
            quantidade = input_float('Quantidade')

            estoque[nome] = estoque.get(nome, 0) + quantidade

            salvar_json(ARQUIVO_ESTOQUE, estoque)

        elif opcao == 1:

            nome = Prompt.ask('Ingrediente').strip().lower()

            if nome in estoque:

                del estoque[nome]

                salvar_json(ARQUIVO_ESTOQUE, estoque)

            else:
                beep('deu ruim')
                console.print('[red]Ingrediente não encontrado[/red]')
                input('Enter...')

        elif opcao == 2:

            nome = Prompt.ask('Ingrediente').strip().lower()

            if nome in estoque:

                quantidade = input_float('Quantidade')

                estoque[nome] -= quantidade

                if estoque[nome] <= 0:
                    del estoque[nome]

                salvar_json(ARQUIVO_ESTOQUE, estoque)

            else:
                beep('deu ruim')
                console.print('[red]Ingrediente não encontrado[/red]')
                input('Enter...')

        elif opcao == 3:

            mostrar_estoque(estoque)

            input('Pressione Enter...')

            beep('ok')

        elif opcao == 4:
            break


def mostrar_receitas(receitas):

    if not receitas:
        console.print('[yellow]Nenhuma receita[/yellow]')
        beep('deu ruim')
        return

    for nome, ingredientes in receitas.items():

        tabela = Table(title=nome)

        tabela.add_column('Ingrediente')
        tabela.add_column('Quantidade')

        for ingrediente, quantidade in ingredientes.items():
            tabela.add_row(ingrediente, str(quantidade))

        console.print(tabela)


def menu_receitas():

    while True:

        receitas = carregar_json(ARQUIVO_RECEITAS)

        opcao = menu_setas(
            [
                'Criar',
                'Remover',
                'Editar',
                'Ver',
                'Voltar'
            ],
            'RECEITAS'
        )

        if opcao == 0:

            nome = Prompt.ask('Nome').strip().lower()

            nova_receita = {}

            while True:

                ingrediente = Prompt.ask(
                    'Ingrediente (fim p/ sair)'
                ).strip().lower()

                if ingrediente == 'fim':
                    break

                quantidade = input_float('Quantidade')

                nova_receita[ingrediente] = quantidade

            receitas[nome] = nova_receita

            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 1:

            nomes = list(receitas.keys())

            if not nomes:
                console.print('[yellow]Sem receitas[/yellow]')
                input('Enter...')
                continue

            indice = menu_setas(nomes, 'Remover receita')

            del receitas[nomes[indice]]

            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 2:

            nomes = list(receitas.keys())

            if not nomes:
                console.print('[yellow]Sem receitas[/yellow]')
                input('Enter...')
                continue

            indice = menu_setas(nomes, 'Editar receita')

            nome_receita = nomes[indice]

            receita = receitas[nome_receita]

            ingredientes = list(receita.keys())

            if not ingredientes:
                console.print('[yellow]Sem ingredientes[/yellow]')
                input('Enter...')
                continue

            ingredientes.append('Voltar')

            indice_ingrediente = menu_setas(
                ingredientes,
                'Escolha ingrediente'
            )

            if ingredientes[indice_ingrediente] == 'Voltar':
                continue

            ingrediente = ingredientes[indice_ingrediente]

            quantidade = input_float('Remover quanto?')

            receita[ingrediente] -= quantidade

            if receita[ingrediente] <= 0:
                del receita[ingrediente]

            receitas[nome_receita] = receita

            salvar_json(ARQUIVO_RECEITAS, receitas)

        elif opcao == 3:

            mostrar_receitas(receitas)

            input('Pressione Enter...')

        elif opcao == 4:
            break


def menu_producao():

    estoque = carregar_json(ARQUIVO_ESTOQUE)
    receitas = carregar_json(ARQUIVO_RECEITAS)

    if not receitas:
        console.print('[yellow]Sem receitas[/yellow]')
        beep('deu ruim')
        input('Enter...')
        return

    nomes = list(receitas.keys())

    nomes.append('Voltar')

    indice = menu_setas(
        nomes,
        'Escolha receita'
    )

    if nomes[indice] == 'Voltar':
        return

    nome_receita = nomes[indice]

    receita = receitas[nome_receita]

    quantidade = input_float('Quantidade')

    for ingrediente, valor in receita.items():

        if estoque.get(ingrediente, 0) < valor * quantidade:

            console.print(
                f'[red]Falta {ingrediente}[/red]'
            )

            beep('deu ruim')

            input('Enter...')

            return

    for ingrediente, valor in receita.items():
        estoque[ingrediente] -= valor * quantidade

    salvar_json(ARQUIVO_ESTOQUE, estoque)

    console.print('[green]Produção concluída[/green]')

    beep('ok')

    input('Enter...')


def main():

    while True:

        opcao = menu_setas(
            [
                'Estoque',
                'Receitas',
                'Produção',
                'Sair'
            ],
            'LoveStock Cake'
        )

        if opcao == 0:
            menu_estoque()

        elif opcao == 1:
            menu_receitas()

        elif opcao == 2:
            menu_producao()

        elif opcao == 3:
            break


if __name__ == '__main__':
    main()
