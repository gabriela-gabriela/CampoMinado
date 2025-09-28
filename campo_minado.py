import campo
import interface
import cronometro
import time
import curses
from curses import wrapper


def movimentar_cursor(tecla, cursor_y, cursor_x, altura, largura):
    # função que movimenta o cursor
    if tecla == curses.KEY_DOWN and cursor_y < altura:
        cursor_y += 1
    elif tecla == curses.KEY_UP and cursor_y > 1:
        cursor_y -= 1
    elif tecla == curses.KEY_LEFT and cursor_x > 2:
        cursor_x -= 2
    elif tecla == curses.KEY_RIGHT and cursor_x < largura * 2 - 1:
        cursor_x += 2
    return cursor_y, cursor_x


def dados_por_dificuldade(opcao_escolhida):
    # função que retorna a altura, largura e quantidade de bombas baseado na dificuldade escolhida
    if opcao_escolhida == "Fácil":
        return 8, 10, 10

    elif opcao_escolhida == "Médio":
        return 14, 18, 40

    elif opcao_escolhida == "Difícil":
        return 20, 24, 100


def jogar(stdscr, altura, largura, bombas, tela):
    # função que contem os loops principais do jogo
    cron = cronometro.Cronometro()
    tempo = "Tempo: 00 s"

    bombas_restantes = bombas
    dados = tempo + f"  Bombas: {bombas_restantes}"
    janela_dados = curses.newwin(
        1, 27, (curses.LINES - altura - 4) // 2, curses.COLS // 2 - 13
    )
    janela_dados.addstr(0, 1, dados)
    janela_dados.refresh()

    rodape = "Mover [←↑↓→] Cavar [c] Marcar bomba [b] Sair [q]"
    stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)
    stdscr.refresh()

    jogo = campo.Campo(altura, largura, bombas)
    casas_vazias = altura * largura - bombas

    janela_jogo = tela.criar_janela(altura, largura, jogo.campo_de_jogo)
    janela_jogo.timeout(1000)

    cursor_y, cursor_x = 1, 1  # posicoes do "cursor" que vai facilitar o jogo

    tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)
    curses.doupdate()

    while True:
        # esse loop é responsável pela primeira jogada, só é possivel mover o cursor e cavar (cavando longe de bombas, em todas as partidas)
        tecla = janela_jogo.getch()

        if tecla == ord("q"):
            stdscr.clear()
            stdscr.refresh()
            return
        elif tecla == ord("c"):
            cron.iniciar()
            jogo.criar_campos(cursor_y - 1, (cursor_x - 1) // 2)
            casas_cavadas = jogo.cavar(cursor_y - 1, (cursor_x - 1) // 2)
            casas_vazias -= casas_cavadas
            break
        elif tecla in [
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
        ]:
            cursor_y, cursor_x = movimentar_cursor(
                tecla, cursor_y, cursor_x, altura, largura
            )

            tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)
            curses.doupdate()

    while True:
        # loop para as jogadas posteriores a primeira, o cronometro é iniciado e agora é permitido marcar bombas
        tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)

        tempo = f"Tempo: {cron.tempo:03d} s"
        dados = tempo + f"  Bombas: {bombas_restantes}"
        janela_dados.addstr(0, 1, dados)
        janela_dados.noutrefresh()

        curses.doupdate()

        tecla = janela_jogo.getch()

        if tecla == ord("q"):
            cron.parar()
            stdscr.clear()
            stdscr.refresh()
            break

        elif tecla == ord("c"):
            casas_cavadas = jogo.cavar(cursor_y - 1, (cursor_x - 1) // 2)
            if casas_cavadas == "gameover":
                cron.parar()
                tela.derrota()
                break

            casas_vazias -= casas_cavadas
            if casas_vazias == 0:
                cron.parar()
                tela.vitoria(tempo)
                break

        elif tecla == ord("b"):
            bombas_restantes += jogo.marcar_bomba(cursor_y - 1, (cursor_x - 1) // 2)

        elif tecla in [
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
        ]:
            cursor_y, cursor_x = movimentar_cursor(
                tecla, cursor_y, cursor_x, altura, largura
            )


def main(stdscr):
    # função principal do jogo, que agrega todas as outras
    if curses.LINES < 32 or curses.COLS < 64:
        print(
            f"Infelizmente o terminal não tem tamanho suficiente para rodar o nosso jogo ):\nTente novamente em um terminal maior para conseguir jogar."
        )
        return

    tela = interface.Interface(stdscr)
    curses.curs_set(0)
    curses.noecho()

    tela.animacao_inicio()

    while True:
        opcao_escolhida = tela.menu()
        if opcao_escolhida == "Jogar":
            dificuldade = tela.menu_dificuldades()
            if dificuldade == "Voltar ao menu":
                continue
            else:
                altura, largura, bombas = dados_por_dificuldade(dificuldade)

        elif opcao_escolhida == "Créditos":
            tela.creditos()
            continue

        elif opcao_escolhida == "Ajuda":
            tela.ajuda()
            continue

        elif opcao_escolhida == "Sair":
            break

        jogar(stdscr, altura, largura, bombas, tela)


if __name__ == "__main__":
    curses.wrapper(main)
