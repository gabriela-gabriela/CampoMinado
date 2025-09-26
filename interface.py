import curses
import time
import random

class Interface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.branco_preto = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.azul_preto = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.vermelho_preto = curses.color_pair(3)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.verde_preto = curses.color_pair(4)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.magenta_preto = curses.color_pair(5)

    def menu(self, stdscr):
        altura_tela, largura_tela = curses.LINES, curses.COLS

        opcoes = ["Fácil", "Médio", "Difícil", "Ajuda e Créditos", "Sair"] # opções que eu quero que o menu tenha
        opcao_escolhida = 0

        altura_janela = 24
        largura_janela = 54
        janela_menu = curses.newwin(altura_janela, largura_janela, altura_tela//2 - altura_janela//2, largura_tela//2 - largura_janela//2)
        janela_menu.keypad(True)

        while True:
            janela_menu.clear()
            janela_menu.border()
            janela_menu.addstr(6, largura_janela//2 - 6, "CAMPO MINADO", curses.A_BOLD|self.azul_preto)
            for i in range(len(opcoes)):
                x = (largura_janela // 2) - len(opcoes[i]) // 2
                y = (altura_janela // 2) - (len(opcoes) // 2) + i * 2
                if i == opcao_escolhida:
                    janela_menu.attron(curses.A_REVERSE)
                    janela_menu.addstr(y, x, opcoes[i])
                    janela_menu.attroff(curses.A_REVERSE)
                else:
                    janela_menu.addstr(y, x, opcoes[i])
            self.stdscr.refresh()
            tecla_clicada = janela_menu.getch()
            janela_menu.refresh()

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
        largura_janela = largura * 2 + 2
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
                if casa == "o":
                    janela.addstr(lin + 1, col * 2 + 1, "  ", curses.A_REVERSE)
                elif casa == "x":
                    janela.addstr(lin + 1, col * 2 + 1, " X", self.vermelho_preto | curses.A_REVERSE)
                elif casa == "1":
                    janela.addstr(lin + 1, col * 2 + 1, " 1", self.azul_preto)
                elif casa == "2":
                    janela.addstr(lin + 1, col * 2 + 1, " 2", self.verde_preto)
                elif casa == "3":
                    janela.addstr(lin + 1, col * 2 + 1, " " + casa, self.vermelho_preto)
                else:
                    janela.addstr(lin + 1, col * 2 + 1, " " + casa, self.magenta_preto)


        janela.addstr(cursor_y, cursor_x, "@@", curses.A_REVERSE)
        janela.refresh()

    def ajuda_creditos(self):
        self.stdscr.clear()
        frase = "parte em andamento, feito por gabriela e lara"
        self.stdscr.addstr(curses.LINES // 2, (curses.COLS - len(frase)) // 2, frase)
        self.stdscr.refresh()
        self.stdscr.getch()
        return

    def animacao_inicio(self):
        # vou fazer uma matriz escrito campo minado e imprimir pra ficar como se fossem as letras so que grandes
        m_campo = [
                [0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,0,0],
                [0,1,1,0,0,1,1,0,0,0,1,1,1,0,0,0,0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0],
                [1,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1],
                [1,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1],
                [0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,1,1,0],
                [0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0]
                ]
        m_minado = [
                [0,1,0,0,0,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0],
                [0,1,1,0,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0],
                [0,1,1,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1],
                [1,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1],
                [1,1,0,1,0,1,1,0,1,1,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,1,1,0],
                [1,1,0,1,0,1,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0]
                ]


        self.stdscr.clear()

        for lin in range(len(m_campo)):
            for col in range(len(m_campo[lin])):
                p = m_campo[lin][col]
                if p == 1:
                    self.stdscr.addstr((curses.LINES // 2) - 7 + lin, ((curses.COLS - len(m_campo[lin])) // 2) + col, " ", curses.A_REVERSE)
                else:
                    self.stdscr.addstr((curses.LINES // 2) - 7 + lin, ((curses.COLS - len(m_campo[lin])) // 2) + col, " ")

        for lin in range(len(m_minado)):
            for col in range(len(m_minado[lin])):
                p = m_minado[lin][col]
                if p == 1:
                    self.stdscr.addstr((curses.LINES // 2) + lin, ((curses.COLS - len(m_minado[lin])) // 2) + col, " ", curses.A_REVERSE) # coloquei reverse mas era melhor que fosse cor eu acho
                else:
                    self.stdscr.addstr((curses.LINES // 2) + lin, ((curses.COLS - len(m_minado[lin])) // 2) + col, " ")

        rodape = "aperte qualquer tecla para iniciar"
        self.stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)

        self.stdscr.refresh()
        self.stdscr.getch()


    def derrota(self):
        altura, largura = self.stdscr.getmaxyx()
        tamanho = altura * largura
        char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
        b = [0] * (tamanho + largura + 1)

        self.stdscr.nodelay(True)
        self.stdscr.timeout(30)

        m_derrota = [
            [1,1,1,1,0,0,0,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0],
            [1,1,1,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0],
            [1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0],
            [1,1,0,0,1,1,0,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0],
            [1,1,1,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1],
            [1,1,1,1,0,0,0,1,1,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1]
        ]

        while True:
            for i in range(int(largura / 9)):
                b[int((random.random() * largura) + largura * (altura - 1))] = 65

            for i in range(tamanho):
                b[i] = int((b[i] + b[i + 1] + b[i + largura] + b[i + largura + 1]) / 4)
                color = (6 if b[i]>15 else (5 if b[i]>9 else (3 if b[i]>4 else 1)))

                if i < tamanho - 1:
                    y, x = int(i / largura), i % largura
                    char_index = min(b[i], len(char) - 1)
                    self.stdscr.addstr(y, x, char[char_index], curses.color_pair(color) | curses.A_BOLD)

            for lin in range(len(m_derrota)):
                for col in range(len(m_derrota[lin])):
                    p = m_derrota[lin][col]
                    y_texto = (altura // 2) - 7 + lin
                    x_texto = ((largura - len(m_derrota[lin])) // 2) + col
                    if p == 1:
                        self.stdscr.addstr(y_texto, x_texto, " ", curses.A_REVERSE)
            rodape = "aperte qualquer tecla para voltar para o menu..."
            self.stdscr.addstr(altura - 3, (largura - len(rodape)) // 2, rodape, curses.A_REVERSE)

            self.stdscr.refresh()
            if self.stdscr.getch() != -1:
                break

        self.stdscr.nodelay(False)
        self.stdscr.timeout(-1)

    def vitoria(self, tempo):
        self.stdscr.clear()
        m_vitoria = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0],
            [1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,1,1,0,0],
            [0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0],
            [0,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1,1,1,1,1,0,0,1,1,0,0,1,1,0,1,1,0],
            [0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,1,1,1,1,1,1,1],
            [0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,1,1,0,0,0,1,1]
        ]
        self.stdscr.clear()
        for lin in range(len(m_vitoria)):
            for col in range(len(m_vitoria[lin])):
                p = m_vitoria[lin][col]
                if p == 1:
                    self.stdscr.addstr((curses.LINES // 2) - 7 + lin, ((curses.COLS - len(m_vitoria[lin])) // 2) + col, " ", curses.A_REVERSE)
                else:
                    self.stdscr.addstr((curses.LINES // 2) - 7 + lin, ((curses.COLS - len(m_vitoria[lin])) // 2) + col, " ")

        self.stdscr.addstr(curses.LINES // 2 + (len(m_vitoria) // 2) + 2, (curses.COLS - len(tempo)) // 2, tempo)

        rodape = "aperte qualquer tecla para voltar para o menu..."
        self.stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)
        self.stdscr.refresh()
        self.stdscr.getch()
