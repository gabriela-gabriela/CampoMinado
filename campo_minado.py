import campo
import interface
import curses
from curses import wrapper


#refazendo tudo:
def main(stdscr):
    tela = interface.Interface(stdscr)
    # apresentar uma animação para o jogador assim que ele abre o programa

    # mostrando o menu para o jogador com as opcoes:
    while True:
        opcao_escolhida = tela.menu(stdscr)
        if opcao_escolhida == "Fácil":
            altura = 8
            largura = 10
            bombas = 10

        elif opcao_escolhida == "Médio":
            altura = 14
            largura = 18
            bombas = 40

        elif opcao_escolhida == "Difícil":
            altura = 20
            largura = 24
            bombas = 40

        elif opcao_escolhida == "Ajuda e Créditos":
            stdscr.clear()
            ajudacreditos = "em andamento, feito por Gabriela e Lara"
            stdscr.addstr(curses.LINES // 2 - len(ajudacreditos) // 2, curses.COLS // 2)
            stdscr.refresh()
            #colocar algo pra sair daqui

        elif opcao_escolhida == "Sair":
            break

        jogo = campo.Campo(altura, largura, bombas)
        jogo.criar_campos()
        janela_jogo = tela.criar_janela(altura, largura, jogo.campo_de_jogo)
        cursor_y, cursor_x = 1, 1 #posicoes do "cursor" que vai facilitar o jogo
        tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)

        #fazer uma primeira jogada separado que cava 0 obrigatoriamente


        casas_vazias = altura * largura - bombas
        while True:
            tela.atualizar_janela(janela_jogo, cursor_y, cursor_x, jogo.campo_de_jogo)

            tecla = janela_jogo.getch()

            if tecla == ord("q"):
                 break

            elif tecla == curses.KEY_DOWN and cursor_y < altura:
                cursor_y += 1
            elif tecla == curses.KEY_UP and cursor_y > 1:
                cursor_y -= 1
            elif tecla == curses.KEY_LEFT and cursor_x > 1:
                cursor_x -= 1
            elif tecla == curses.KEY_RIGHT and cursor_x < largura:
                cursor_x += 1

            elif tecla == ord("c"):
                casas_cavadas = jogo.cavar(cursor_y - 1, cursor_x - 1)
                if casas_cavadas == "gameover":
                    tela.game_over()
                    
                casas_vazias -= casas_cavadas
                if casas_vazias == 0:
                    tela.vitoria()

            elif tecla == ord("m"):
                jogo.marcar_bomba(cursor_y - 1, cursor_x - 1)


curses.wrapper(main)
