import campo
import interface
import curses
from curses import wrapper


def movimentar_cursor(tecla, cursor_y, cursor_x, altura, largura):
    if tecla == curses.KEY_DOWN and cursor_y < altura:
        cursor_y += 1
    elif tecla == curses.KEY_UP and cursor_y > 1:
        cursor_y -= 1
    elif tecla == curses.KEY_LEFT and cursor_x > 2:
        cursor_x -= 2
    elif tecla == curses.KEY_RIGHT and cursor_x < largura * 2:
        cursor_x += 2
    return cursor_y, cursor_x

def dados_por_dificuldade(opcao_escolhida):
    if opcao_escolhida == "Fácil":
        return 8, 10, 10

    elif opcao_escolhida == "Médio":
        return 14, 18, 40

    elif opcao_escolhida == "Difícil":
        return 20, 24, 100

def jogar(altura, largura, bombas, tela):
    jogo = campo.Campo(altura, largura, bombas)
    casas_vazias = altura * largura - bombas
    janela_jogo = tela.criar_janela(altura, largura, jogo.campo_de_jogo)
    cursor_y, cursor_x = 1, 1 #posicoes do "cursor" que vai facilitar o jogo
    tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)


    #fazer uma primeira jogada separado que cava 0 obrigatoriamente
    while True:
        tecla = janela_jogo.getch()
        if tecla == ord("q"):
            return #aqui vai pra segunda jogada sendo que era pra voltar pra o menu
        elif tecla == ord("c"):
            jogo.criar_campos(cursor_y - 1, (cursor_x - 1) // 2)
            casas_cavadas = jogo.cavar(cursor_y - 1, (cursor_x - 1) // 2)
            casas_vazias -= casas_cavadas
            break
        elif tecla in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            cursor_y, cursor_x = movimentar_cursor(tecla, cursor_y, cursor_x, altura, largura)

            tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)

    # esse loop aqui embaixo é pra as jogadas a partir da segunda
    while True:
        tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)

        tecla = janela_jogo.getch()

        if tecla == ord("q"):
            break

        elif tecla == ord("c"):
            casas_cavadas = jogo.cavar(cursor_y - 1, (cursor_x - 1) // 2)
            if casas_cavadas == "gameover":
                tela.game_over()
                break

            casas_vazias -= casas_cavadas
            if casas_vazias == 0:
                tela.vitoria()
                break

        elif tecla == ord("m"):
            jogo.marcar_bomba(cursor_y - 1, (cursor_x - 1) // 2)

        elif tecla in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            cursor_y, cursor_x = movimentar_cursor(tecla, cursor_y, cursor_x, altura, largura)


#refazendo tudo:
def main(stdscr):
    #tem q por uma verificao pra ver se o tamanho do terminal é grande o suficiente
    tela = interface.Interface(stdscr)
    curses.curs_set(0)
    curses.noecho()

    # apresentar uma animação para o jogador assim que ele abre o programa
    tela.animacao_inicio()

    while True:
        # mostra o menu pra o jogador
        opcao_escolhida = tela.menu(stdscr)
        if opcao_escolhida == "Ajuda e Créditos":
            tela.ajuda_creditos()
            continue

        elif opcao_escolhida == "Sair":
            break

        else:
            altura, largura, bombas = dados_por_dificuldade(opcao_escolhida)

        jogar(altura, largura, bombas, tela)


curses.wrapper(main)
