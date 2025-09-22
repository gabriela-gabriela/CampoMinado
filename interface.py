import curses

class Interface:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def menu(self, stdscr):
        self.stdscr.clear()
        altura_tela, largura_tela = curses.LINES, curses.COLS

        opcoes = ["Fácil", "Médio", "Díficil", "Ajuda e Créditos", "Sair"] # opções que eu quero que o menu tenha
        opcao_escolhida = 0

        while True:
            self.stdscr.clear()
            for i in range(len(opcoes)):
                x = (largura_tela // 2) - len(opcoes[i]) // 2
                y = (altura_tela // 2) - (len(opcoes) // 2) + i * 2
                if i == opcao_escolhida:
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(y, x, opcoes[i])
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, opcoes[i])

            self.stdscr.refresh()

            tecla_clicada = self.stdscr.getch()

            if tecla_clicada == curses.KEY_DOWN and opcao_escolhida < len(opcoes) - 1:
                opcao_escolhida += 1
            elif tecla_clicada == curses.KEY_UP and opcao_escolhida > 0:
                opcao_escolhida -= 1

            elif tecla_clicada in [curses.KEY_ENTER, 10, 13]:
                self.stdscr.clear()
                self.stdscr.refresh()
                return opcoes[opcao_escolhida]

    def criar_janela(self, altura, largura, campo_de_jogo):
        # aumentando um pouco a altura e largura baseado no campo pra poder caber dentro da borda
        altura_janela = altura + 2
        largura_janela = largura + 2
        y_janela = (curses.LINES // 2) - (altura_janela // 2)
        x_janela = (curses.COLS // 2) - (largura_janela // 2)
        janela = curses.newwin(altura_janela, largura_janela, y_janela, x_janela)
        janela.keypad(True)

        return janela

    def atualizar_janela(self, janela, cursor_y, cursor_x, campo_de_jogo):
        janela.clear()
        janela.border()
        for lin in range(len(campo_de_jogo)):
            for col in range(len(campo_de_jogo[lin])):
                casa = campo_de_jogo[lin][col]
                if casa == None:
                    casa = "o"
                janela.addch(lin + 1, col + 1, casa)

        janela.addch(cursor_y, cursor_x, "@", curses.A_REVERSE)
        janela.refresh()


    def game_over(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Voce perdeu")
        self.stdscr.refresh()

        #animacao de explosao
        #voce perdeu na tela
        #mostra o "gabarito" do campo minado
        #opcao de voltar pra o menu

    def vitoria(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Voce ganhou")
        self.stdscr.refresh()

        #alguma animacaozinha de vitoria
        #voce ganhou na tela
        #opcao de voltar pra o menu
