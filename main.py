# ============================================================
# LOVESTOCK CAKE
# Sistema simples de controle de estoque, receitas e produção
# ============================================================


# ------------------------------------------------------------
# IMPORTAÇÕES
# ------------------------------------------------------------

import time       # Permite fazer pausas usando time.sleep()
import winsound   # Permite emitir sons no Windows
import json       # Permite trabalhar com arquivos JSON
import os         # Permite verificar arquivos e executar comandos do sistema
import msvcrt     # Permite capturar teclas diretamente do teclado


# Importações da biblioteca Rich
from rich.console import Console   # Responsável pelas mensagens no terminal
from rich.table import Table       # Permite criar tabelas
from rich.panel import Panel       # Permite criar painéis
from rich.prompt import Prompt     # Facilita a entrada de dados


# Cria o objeto que será usado para imprimir no terminal
console = Console()


# ------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------

# Arquivo onde os ingredientes do estoque serão armazenados
ARQUIVO_ESTOQUE = "estoque.json"

# Arquivo onde as receitas serão armazenadas
ARQUIVO_RECEITAS = "receita.json"


# ------------------------------------------------------------
# FUNÇÃO DE SONS
# ------------------------------------------------------------

def beep(tipo='ok'):
    """
    Emite sons diferentes dependendo da situação.

    Tipos:
        'ok'       -> som de sucesso
        'deu ruim' -> som de erro
        'click'    -> som de navegação
    """

    # Som utilizado quando uma operação deu certo
    if tipo == 'ok':

        winsound.Beep(1000, 100)
        winsound.Beep(1300, 150)
        winsound.Beep(900, 100)

    # Som utilizado quando aconteceu algum erro
    elif tipo == 'deu ruim':

        winsound.Beep(700, 100)

        # Pequena pausa entre os sons
        time.sleep(0.05)

        winsound.Beep(500, 120)

        time.sleep(0.05)

        winsound.Beep(300, 180)

    # Som curto utilizado ao navegar pelo menu
    elif tipo == 'click':

        winsound.Beep(1000, 30)

        time.sleep(0.01)

        winsound.Beep(800, 20)


# ------------------------------------------------------------
# MENU COM SETAS
# ------------------------------------------------------------

def menu_setas(opcoes, titulo=''):
    """
    Cria um menu que pode ser controlado pelas setas do teclado.

    Parâmetros:
        opcoes -> lista contendo as opções do menu
        titulo -> título que aparecerá no painel

    Retorna:
        índice da opção escolhida
    """

    # Começamos selecionando a primeira opção
    atual = 0

    # O menu continua funcionando até o usuário apertar Enter
    while True:

        # Limpa o terminal.
        # 'cls' funciona no Windows.
        os.system('cls')

        # Lista que armazenará as linhas que serão mostradas
        linhas = []

        # Percorre todas as opções do menu
        for i, opcao in enumerate(opcoes):

            # Se essa for a opção selecionada...
            if i == atual:

                # Mostra um coração indicando a opção atual
                linhas.append(
                    f'[#ff69b4] ❤️   {opcao}[/]'
                )

            else:

                # Opções não selecionadas aparecem normalmente
                linhas.append(
                    f' {opcao}'
                )

        # Cria um painel usando o Rich
        console.print(
            Panel(
                '\n'.join(linhas),
                title=titulo,
                style="#e7b7cf"
            )
        )

        # Espera o usuário apertar alguma tecla
        tecla = msvcrt.getch()

        # As setas do teclado no Windows começam com b'\xe0'
        if tecla == b'\xe0':

            # Lê a segunda parte da tecla
            tecla = msvcrt.getch()

            # Tecla H representa seta para cima
            if tecla == b'H':

                atual -= 1

                # Toca o som de navegação
                beep('click')

            # Tecla P representa seta para baixo
            elif tecla == b'P':

                atual += 1

                beep('click')

        # Enter
        elif tecla == b'\r':

            # Som de confirmação
            beep('ok')

            # Retorna a posição escolhida
            return atual

        # O operador % faz o menu voltar para o começo
        # quando chegamos ao final, ou ir para o final
        # quando passamos do primeiro item.
        atual %= len(opcoes)


# ------------------------------------------------------------
# CARREGAR JSON
# ------------------------------------------------------------

def carregar_json(nome_arquivo):
    """
    Abre um arquivo JSON e transforma seu conteúdo
    em um objeto Python.

    Caso o arquivo não exista, retorna um dicionário vazio.
    """

    try:

        # Verifica se o arquivo não existe
        if not os.path.exists(nome_arquivo):

            # Se não existe, começamos com dados vazios
            return {}

        # Abre o arquivo no modo leitura
        with open(
            nome_arquivo,
            'r',
            encoding='utf-8'
        ) as arquivo:

            # json.load() transforma o JSON em Python
            return json.load(arquivo)

    # Caso o arquivo tenha um JSON inválido
    except json.JSONDecodeError:

        beep('deu ruim')

        console.print(
            f'[red]JSON inválido em {nome_arquivo}[/red]'
        )

        return {}

    # Caso aconteça qualquer outro erro
    except Exception as e:

        beep('deu ruim')

        console.print(
            f'[red]Erro ao carregar: {e}[/red]'
        )

        return {}


# ------------------------------------------------------------
# SALVAR JSON
# ------------------------------------------------------------

def salvar_json(nome_arquivo, dados):
    """
    Salva dados Python dentro de um arquivo JSON.
    """

    # Abre o arquivo no modo escrita
    with open(
        nome_arquivo,
        'w',
        encoding='utf-8'
    ) as arquivo:

        # Converte o objeto Python para JSON
        json.dump(
            dados,
            arquivo,

            # Permite salvar caracteres como ç e ã
            ensure_ascii=False,

            # Deixa o JSON organizado e indentado
            indent=4
        )

    # Som de sucesso
    beep('ok')


# ------------------------------------------------------------
# RECEBER NÚMERO DECIMAL
# ------------------------------------------------------------

def input_float(mensagem):
    """
    Solicita ao usuário um número decimal.

    O programa continua perguntando até receber
    um número válido maior que zero.
    """

    while True:

        try:

            # Mostra a pergunta para o usuário
            valor = Prompt.ask(mensagem)

            # Permite que o usuário digite:
            #
            # 2.5
            #
            # ou
            #
            # 2,5
            #
            # O replace transforma vírgula em ponto.
            numero = float(
                valor.replace(",", ".")
            )

            # Não permitimos números menores ou iguais a zero
            if numero <= 0:

                beep('deu ruim')

                console.print(
                    '[red]Digite um número maior que zero[/red]'
                )

                # Volta para o começo do while
                continue

            # Número válido
            return numero

        # Se não for possível transformar o valor em float
        except:

            beep('deu ruim')

            console.print(
                '[red]Número inválido[/red]'
            )


# ------------------------------------------------------------
# MOSTRAR ESTOQUE
# ------------------------------------------------------------

def mostrar_estoque(estoque):
    """
    Exibe todos os ingredientes disponíveis
    em uma tabela.
    """

    # Cria uma tabela
    tabela = Table(title='Estoque')

    # Cria as colunas
    tabela.add_column('Ingrediente')
    tabela.add_column('Quantidade')

    # Verifica se o estoque está vazio
    if not estoque:

        console.print(
            '[yellow]Estoque vazio[/yellow]'
        )

        return

    # Percorre todos os ingredientes
    for ingrediente, quantidade in estoque.items():

        # Adiciona uma linha na tabela
        tabela.add_row(
            ingrediente.title(),
            str(quantidade)
        )

    # Mostra a tabela
    console.print(tabela)


# ------------------------------------------------------------
# MENU DE ESTOQUE
# ------------------------------------------------------------

def menu_estoque():
    """
    Controla todas as operações relacionadas ao estoque.

    Opções:
        Adicionar
        Remover total
        Remover quantidade
        Ver estoque
        Voltar
    """

    # O menu fica funcionando até o usuário escolher Voltar
    while True:

        # Carrega o estoque atual
        estoque = carregar_json(
            ARQUIVO_ESTOQUE
        )

        # Mostra o menu
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

        # ----------------------------------------------------
        # ADICIONAR INGREDIENTE
        # ----------------------------------------------------

        if opcao == 0:

            # Solicita o nome do ingrediente
            nome = Prompt.ask(
                'Ingrediente'
            ).strip().lower()

            # Solicita a quantidade
            quantidade = input_float(
                'Quantidade'
            )

            # .get(nome, 0):
            #
            # Se o ingrediente já existe,
            # pega sua quantidade atual.
            #
            # Se não existe,
            # começa com 0.
            #
            # Depois adicionamos a nova quantidade.
            estoque[nome] = (
                estoque.get(nome, 0)
                + quantidade
            )

            # Salva o estoque atualizado
            salvar_json(
                ARQUIVO_ESTOQUE,
                estoque
            )

        # ----------------------------------------------------
        # REMOVER INGREDIENTE COMPLETAMENTE
        # ----------------------------------------------------

        elif opcao == 1:

            nome = Prompt.ask(
                'Ingrediente'
            ).strip().lower()

            # Verifica se o ingrediente existe
            if nome in estoque:

                # del remove completamente o ingrediente
                del estoque[nome]

                # Salva a alteração
                salvar_json(
                    ARQUIVO_ESTOQUE,
                    estoque
                )

            else:

                beep('deu ruim')

                console.print(
                    '[red]Ingrediente não encontrado[/red]'
                )

                input('Enter...')

        # ----------------------------------------------------
        # REMOVER UMA QUANTIDADE
        # ----------------------------------------------------

        elif opcao == 2:

            nome = Prompt.ask(
                'Ingrediente'
            ).strip().lower()

            # Verifica se o ingrediente existe
            if nome in estoque:

                # Pergunta quanto será removido
                quantidade = input_float(
                    'Quantidade'
                )

                # Diminui a quantidade do estoque
                estoque[nome] -= quantidade

                # Arredonda para duas casas decimais
                estoque[nome] = round(
                    estoque[nome],
                    2
                )

                # Se acabou o ingrediente,
                # removemos ele do dicionário.
                if estoque[nome] <= 0:

                    del estoque[nome]

                # Salva o estoque
                salvar_json(
                    ARQUIVO_ESTOQUE,
                    estoque
                )

            else:

                beep('deu ruim')

                console.print(
                    '[red]Ingrediente não encontrado[/red]'
                )

                input('Enter...')

        # ----------------------------------------------------
        # VISUALIZAR ESTOQUE
        # ----------------------------------------------------

        elif opcao == 3:

            # Mostra a tabela
            mostrar_estoque(estoque)

            input('Pressione Enter...')

            beep('ok')

        # ----------------------------------------------------
        # VOLTAR
        # ----------------------------------------------------

        elif opcao == 4:

            break


# ------------------------------------------------------------
# MOSTRAR RECEITAS
# ------------------------------------------------------------

def mostrar_receitas(receitas):
    """
    Mostra todas as receitas cadastradas.
    """

    # Verifica se não existem receitas
    if not receitas:

        console.print(
            '[yellow]Nenhuma receita[/yellow]'
        )

        beep('deu ruim')

        return

    # Percorre todas as receitas
    for nome, ingredientes in receitas.items():

        # Cria uma tabela para cada receita
        tabela = Table(
            title=nome.replace('_', ' ').title()
        )

        # Cria as colunas
        tabela.add_column('Ingrediente')
        tabela.add_column('Quantidade')

        # Percorre os ingredientes da receita
        for ingrediente, quantidade in ingredientes.items():

            tabela.add_row(
                ingrediente.title(),
                str(quantidade)
            )

        # Exibe a tabela
        console.print(tabela)


# ------------------------------------------------------------
# MENU DE RECEITAS
# ------------------------------------------------------------

def menu_receitas():
    """
    Controla as operações relacionadas às receitas.

    Opções:
        Criar
        Remover
        Editar
        Ver
        Voltar
    """

    while True:

        # Carrega as receitas salvas
        receitas = carregar_json(
            ARQUIVO_RECEITAS
        )

        # Mostra o menu
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

        # ----------------------------------------------------
        # CRIAR RECEITA
        # ----------------------------------------------------

        if opcao == 0:

            # Nome da receita
            nome = Prompt.ask(
                'Nome'
            ).strip().lower()

            # Dicionário que armazenará
            # os ingredientes da receita
            nova = {}

            # Continua adicionando ingredientes
            while True:

                ingrediente = Prompt.ask(
                    'Ingrediente (fim p/ sair)'
                ).strip().lower()

                # A palavra "fim" encerra o cadastro
                if ingrediente == 'fim':

                    break

                # Quantidade necessária
                quantidade = input_float(
                    'Quantidade'
                )

                # Adiciona ingrediente e quantidade
                nova[ingrediente] = quantidade

            # Salva a nova receita
            receitas[nome] = nova

            # Atualiza o arquivo JSON
            salvar_json(
                ARQUIVO_RECEITAS,
                receitas
            )

        # ----------------------------------------------------
        # REMOVER RECEITA
        # ----------------------------------------------------

        elif opcao == 1:

            # Cria uma lista com os nomes das receitas
            nomes = list(receitas.keys())

            # Se não houver receitas
            if not nomes:

                console.print(
                    '[yellow]Sem receitas[/yellow]'
                )

                input('Enter...')

                continue

            # Mostra as receitas no menu
            indice = menu_setas(
                nomes,
                'Remover receita'
            )

            # Remove a receita escolhida
            del receitas[nomes[indice]]

            # Salva as alterações
            salvar_json(
                ARQUIVO_RECEITAS,
                receitas
            )

        # ----------------------------------------------------
        # EDITAR RECEITA
        # ----------------------------------------------------

        elif opcao == 2:

            # Lista os nomes das receitas
            nomes = list(receitas.keys())

            # Verifica se existem receitas
            if not nomes:

                console.print(
                    '[yellow]Sem receitas[/yellow]'
                )

                input('Enter...')

                continue

            # Escolhe qual receita será editada
            indice = menu_setas(
                nomes,
                'Editar receita'
            )

            # Pega o nome da receita escolhida
            nome = nomes[indice]

            # Pega os ingredientes dessa receita
            receita = receitas[nome]

            # Cria uma lista com os ingredientes
            ingredientes = list(
                receita.keys()
            )

            # Se a receita não tiver ingredientes
            if not ingredientes:

                console.print(
                    '[yellow]Sem ingredientes[/yellow]'
                )

                input('Enter...')

                continue

            # Adiciona uma opção para voltar
            ingredientes.append('Voltar')

            # Mostra os ingredientes no menu
            indice_ingrediente = menu_setas(
                ingredientes,
                'Escolha ingrediente'
            )

            # Se o usuário escolher Voltar
            if ingredientes[indice_ingrediente] == 'Voltar':

                continue

            # Pega o ingrediente escolhido
            ingrediente = ingredientes[
                indice_ingrediente
            ]

            # Pergunta quanto será removido
            quantidade = input_float(
                'Remover quanto?'
            )

            # Diminui a quantidade do ingrediente
            receita[ingrediente] -= quantidade

            # Arredonda para duas casas
            receita[ingrediente] = round(
                receita[ingrediente],
                2
            )

            # Se a quantidade chegou a zero,
            # remove o ingrediente da receita
            if receita[ingrediente] <= 0:

                del receita[ingrediente]

            # Atualiza a receita
            receitas[nome] = receita

            # Salva as alterações
            salvar_json(
                ARQUIVO_RECEITAS,
                receitas
            )

        # ----------------------------------------------------
        # VISUALIZAR RECEITAS
        # ----------------------------------------------------

        elif opcao == 3:

            mostrar_receitas(receitas)

            input('Pressione Enter...')

        # ----------------------------------------------------
        # VOLTAR
        # ----------------------------------------------------

        elif opcao == 4:

            break


# ------------------------------------------------------------
# MENU DE PRODUÇÃO
# ------------------------------------------------------------

def menu_producao():
    """
    Realiza a produção de uma receita.

    O programa verifica primeiro se existe quantidade
    suficiente de cada ingrediente no estoque.

    Se existir:
        -> desconta os ingredientes do estoque.

    Se faltar:
        -> informa qual ingrediente está faltando.
    """

    # Carrega o estoque
    estoque = carregar_json(
        ARQUIVO_ESTOQUE
    )

    # Carrega as receitas
    receitas = carregar_json(
        ARQUIVO_RECEITAS
    )

    # Verifica se existem receitas cadastradas
    if not receitas:

        console.print(
            '[yellow]Sem receitas[/yellow]'
        )

        beep('deu ruim')

        input('Enter...')

        return

    # Lista com os nomes das receitas
    nomes = list(receitas.keys())

    # Adiciona uma opção para voltar
    nomes.append('Voltar')

    # Mostra as receitas
    indice = menu_setas(
        nomes,
        'Escolha receita'
    )

    # Se o usuário escolher Voltar
    if nomes[indice] == 'Voltar':

        return

    # Nome da receita escolhida
    nome = nomes[indice]

    # Ingredientes e quantidades da receita
    receita = receitas[nome]

    # Pergunta quantas unidades serão produzidas
    quantidade = input_float(
        'Quantidade'
    )

    # --------------------------------------------------------
    # PRIMEIRA ETAPA:
    # VERIFICAR SE EXISTEM INGREDIENTES SUFICIENTES
    # --------------------------------------------------------

    for ingrediente, valor in receita.items():

        # Calcula quanto será necessário
        #
        # Exemplo:
        #
        # Receita precisa de 2 ovos
        # Produção = 3
        #
        # necessário = 2 * 3 = 6 ovos
        necessario = valor * quantidade

        # Pega a quantidade disponível no estoque
        #
        # Se não existir, considera 0.
        disponivel = estoque.get(
            ingrediente,
            0
        )

        # Verifica se o estoque é insuficiente
        if disponivel < necessario:

            # Calcula quanto está faltando
            faltando = (
                necessario - disponivel
            )

            console.print(
                f'[red]Falta {faltando:.2f} de '
                f'{ingrediente.title()}[/red]'
            )

            beep('deu ruim')

            input('Enter...')

            # Cancela a produção
            return

    # --------------------------------------------------------
    # SEGUNDA ETAPA:
    # DESCONTAR INGREDIENTES DO ESTOQUE
    # --------------------------------------------------------

    for ingrediente, valor in receita.items():

        # Desconta do estoque a quantidade utilizada
        estoque[ingrediente] -= (
            valor * quantidade
        )

        # Arredonda para duas casas decimais
        estoque[ingrediente] = round(
            estoque[ingrediente],
            2
        )

        # Se o ingrediente acabou,
        # removemos ele do estoque.
        if estoque[ingrediente] <= 0:

            del estoque[ingrediente]

    # Salva o novo estoque
    salvar_json(
        ARQUIVO_ESTOQUE,
        estoque
    )

    # Mensagem de sucesso
    console.print(
        '[green]Produção concluída[/green]'
    )

    beep('ok')

    input('Enter...')


# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def main():
    """
    Função principal do programa.

    É responsável por mostrar o menu inicial
    e direcionar o usuário para cada área do sistema.
    """

    # O programa fica rodando até o usuário escolher Sair
    while True:

        # Menu principal
        opcao = menu_setas(
            [
                'Estoque',
                'Receitas',
                'Produção',
                'Sair'
            ],
            'LoveStock Cake'
        )

        # ----------------------------------------------------
        # ESTOQUE
        # ----------------------------------------------------

        if opcao == 0:

            menu_estoque()

        # ----------------------------------------------------
        # RECEITAS
        # ----------------------------------------------------

        elif opcao == 1:

            menu_receitas()

        # ----------------------------------------------------
        # PRODUÇÃO
        # ----------------------------------------------------

        elif opcao == 2:

            menu_producao()

        # ----------------------------------------------------
        # SAIR
        # ----------------------------------------------------

        elif opcao == 3:

            break


# ------------------------------------------------------------
# INÍCIO DO PROGRAMA
# ------------------------------------------------------------

# Essa condição verifica se este arquivo está sendo
# executado diretamente.
#
# Se estiver, chama a função main().
if __name__ == '__main__':

    main()
