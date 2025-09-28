import curses
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
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.amarelo_preto = curses.color_pair(6)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.ciano_preto = curses.color_pair(7)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_RED)
        self.preto_vermelho = curses.color_pair(8)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.preto_branco = curses.color_pair(9)

    def menu(self):
        # função para mostrar o menu para o jogador
        self.stdscr.clear()
        altura_tela, largura_tela = curses.LINES, curses.COLS

        opcoes = [
            "Jogar",
            "Ajuda",
            "Créditos",
            "Sair",
        ]  # opções que eu quero que o menu tenha
        opcao_escolhida = 0

        altura_janela = 24
        largura_janela = 32
        janela_menu = curses.newwin(
            altura_janela,
            largura_janela,
            altura_tela // 2 - altura_janela // 2,
            largura_tela // 2 - largura_janela // 2,
        )
        janela_menu.keypad(True)

        while True:
            janela_menu.border()
            janela_menu.addstr(
                6,
                largura_janela // 2 - 6,
                "CAMPO MINADO",
                curses.A_BOLD | self.azul_preto,
            )
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

    def menu_dificuldades(self):
        # função para mostrar o menu de dificuldades para o jogador
        altura_tela, largura_tela = curses.LINES, curses.COLS

        dificuldades = ["Fácil", "Médio", "Difícil", "Voltar ao menu"]

        opcao_escolhida = 0

        altura_janela = 16
        largura_janela = 24
        janela_dificuldades = curses.newwin(
            altura_janela,
            largura_janela,
            altura_tela // 2 - altura_janela // 2,
            largura_tela // 2 - largura_janela // 2,
        )
        janela_dificuldades.keypad(True)

        while True:
            janela_dificuldades.border()
            janela_dificuldades.addstr(
                3,
                largura_janela // 2 - 6,
                "CAMPO MINADO",
                curses.A_BOLD | self.azul_preto,
            )
            for i in range(len(dificuldades)):
                x = (largura_janela // 2) - len(dificuldades[i]) // 2
                y = (altura_janela // 2) - (len(dificuldades) // 2) + i * 2
                if i == opcao_escolhida:
                    janela_dificuldades.attron(curses.A_REVERSE)
                    janela_dificuldades.addstr(y, x, dificuldades[i])
                    janela_dificuldades.attroff(curses.A_REVERSE)
                else:
                    janela_dificuldades.addstr(y, x, dificuldades[i])
            self.stdscr.refresh()
            tecla_clicada = janela_dificuldades.getch()
            janela_dificuldades.refresh()

            if (
                tecla_clicada == curses.KEY_DOWN
                and opcao_escolhida < len(dificuldades) - 1
            ):
                opcao_escolhida += 1
            elif tecla_clicada == curses.KEY_UP and opcao_escolhida > 0:
                opcao_escolhida -= 1

            elif tecla_clicada in [curses.KEY_ENTER, 10, 13]:
                self.stdscr.clear()
                self.stdscr.refresh()
                return dificuldades[opcao_escolhida]

    def criar_janela(self, altura, largura, campo_de_jogo):
        # função que cria a janela de jogo baseado no dificuldade
        altura_janela = altura + 2
        largura_janela = largura * 2 + 2
        y_janela = (curses.LINES // 2) - (altura_janela // 2)
        x_janela = (curses.COLS // 2) - (largura_janela // 2)
        janela = curses.newwin(altura_janela, largura_janela, y_janela, x_janela)
        janela.keypad(True)

        return janela

    def atualizar_janela(self, janela, cursor_y, cursor_x, campo_de_jogo):
        # função que atualiza a janeça do jogo
        janela.border()
        for lin in range(len(campo_de_jogo)):
            for col in range(len(campo_de_jogo[lin])):
                casa = campo_de_jogo[lin][col]
                if casa == None:
                    casa = "o"
                if casa == "o":
                    janela.addstr(lin + 1, col * 2 + 1, "  ", curses.A_REVERSE)
                elif casa == "x":
                    janela.addstr(
                        lin + 1,
                        col * 2 + 1,
                        " X",
                        self.vermelho_preto | curses.A_REVERSE,
                    )
                elif casa == "1":
                    janela.addstr(lin + 1, col * 2 + 1, " 1", self.azul_preto)
                elif casa == "2":
                    janela.addstr(lin + 1, col * 2 + 1, " 2", self.verde_preto)
                elif casa == "3":
                    janela.addstr(lin + 1, col * 2 + 1, " " + casa, self.vermelho_preto)
                else:
                    janela.addstr(lin + 1, col * 2 + 1, " " + casa, self.magenta_preto)

            casa = campo_de_jogo[cursor_y - 1][(cursor_x - 1) // 2]
            if casa == None:
                casa = "o"
            if casa == " ":
                cursor = ["  ", self.branco_preto]
            elif casa == "o":
                cursor = ["  ", self.preto_branco]
            elif casa == "x":
                cursor = [" X", self.preto_vermelho]
            elif casa == "1":
                cursor = [" 1", self.azul_preto]
            elif casa == "2":
                cursor = [" 2", self.verde_preto]
            elif casa == "3":
                cursor = [" 3", self.vermelho_preto]
            else:
                cursor = [" " + casa, self.magenta_preto]

        janela.addstr(cursor_y, cursor_x, cursor[0], cursor[1] | curses.A_REVERSE)
        janela.noutrefresh()

    def creditos(self):
        # função que mostra a tela de ajuda com as instruções de jogo para o jogador
        self.stdscr.clear()
        self.stdscr.addstr(
            curses.LINES // 2 - 8,
            curses.COLS // 2 - 4,
            "CRÉDITOS",
            self.amarelo_preto | curses.A_BOLD,
        )

        self.stdscr.addstr(
            curses.LINES // 2 - 6,
            curses.COLS // 2 - 6,
            "professores",
            self.verde_preto | curses.A_BOLD,
        )
        professores = ["Dalton Serey", "Jorge", "Wilkerson"]
        for i in range(len(professores)):
            self.stdscr.addstr(
                curses.LINES // 2 - 5 + i, curses.COLS // 2 - 8, professores[i]
            )

        self.stdscr.addstr(
            curses.LINES // 2 - 1,
            curses.COLS // 2 - 4,
            "monitor",
            self.azul_preto | curses.A_BOLD,
        )
        self.stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 8, "glima")

        self.stdscr.addstr(
            curses.LINES // 2 + 2,
            curses.COLS // 2 - 7,
            "programadoras",
            self.magenta_preto | curses.A_BOLD,
        )
        programadoras = ["Lara Soares", "Gabriela Ramalho"]
        for i in range(len(programadoras)):
            self.stdscr.addstr(
                curses.LINES // 2 + 3 + i, curses.COLS // 2 - 8, programadoras[i]
            )

        self.stdscr.addstr(
            curses.LINES // 2 + 6,
            curses.COLS // 2 - 8,
            "Animação do fogo",
            self.vermelho_preto | curses.A_BOLD,
        )
        self.stdscr.addstr(
            curses.LINES // 2 + 7, curses.COLS // 2 - 8, "Chris Simpkins"
        )

        rodape = "aperte qualquer tecla para voltar ao menu"
        self.stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)
        self.stdscr.refresh()
        self.stdscr.getch()
        self.stdscr.clear()
        self.stdscr.refresh()

    def ajuda(self):
        # função que mostra a tela de ajuda com as instruções de jogo para o jogador
        self.stdscr.clear()
        self.stdscr.addstr(
            curses.LINES // 2 - 11,
            curses.COLS // 2 - 5,
            "COMO JOGAR",
            self.amarelo_preto | curses.A_BOLD,
        )
        frases = [
            "Objetivo: revelar todos os espaços que não possuem",
            "bombas",
            "Sobre as casas:",
            "casas vazias não possuem bombas (cada casa ocupa o",
            "espaco de dois caracteres no terminal;",
            "casas com números indicam o número de bombas nas casas",
            "ao redor;",
            "casas vermelhas representam bombas que você marcou e",
            "não podem ser cavadas.",
            "Outras coisas importantes:",
            "o tempo só começa após cavar a primeira casa (tente",
            "conseguir o melhor tempo!)",
            "cavar uma casa de número x - caso tenham x casas",
            "marcadas ao redor - cava as casas adjacentes não",
            "marcadas",
            "agora que você sabe o básico, pode começar a diversão!",
            "mas sempre lembre, seja inteligente e faça um plano!!!",
        ]

        for i in range(len(frases)):
            self.stdscr.addstr(
                curses.LINES // 2 - 9 + i, curses.COLS // 2 - 28, frases[i]
            )

        self.stdscr.addstr(
            curses.LINES // 2 - 9, curses.COLS // 2 - 28, "Objetivo:", self.verde_preto
        )
        self.stdscr.addstr(
            curses.LINES // 2 - 7,
            curses.COLS // 2 - 28,
            "Sobre as casas:",
            self.azul_preto,
        )
        self.stdscr.addstr(
            curses.LINES // 2,
            curses.COLS // 2 - 28,
            "Outras coisas importantes:",
            self.magenta_preto,
        )
        self.stdscr.addstr(
            curses.LINES // 2 + 7,
            curses.COLS // 2 + 10,
            "faça um plano!!!",
            self.vermelho_preto | curses.A_BOLD,
        )

        rodape = "aperte qualquer tecla pra voltar ao menu"
        self.stdscr.addstr(
            curses.LINES // 2 + 11, (curses.COLS - len(rodape)) // 2, rodape
        )
        self.stdscr.getch()
        self.stdscr.clear()
        self.stdscr.refresh()

    def animacao_inicio(self):
        # função que mostra o desenho inicial do "campo minado" para o jogador

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
                    self.stdscr.addstr(
                        (curses.LINES // 2) - 7 + lin,
                        ((curses.COLS - len(m_campo[lin])) // 2) + col,
                        " ",
                        curses.A_REVERSE,
                    )
                else:
                    self.stdscr.addstr(
                        (curses.LINES // 2) - 7 + lin,
                        ((curses.COLS - len(m_campo[lin])) // 2) + col,
                        " ",
                    )

        for lin in range(len(m_minado)):
            for col in range(len(m_minado[lin])):
                p = m_minado[lin][col]
                if p == 1:
                    self.stdscr.addstr(
                        (curses.LINES // 2) + lin,
                        ((curses.COLS - len(m_minado[lin])) // 2) + col,
                        " ",
                        curses.A_REVERSE,
                    )
                else:
                    self.stdscr.addstr(
                        (curses.LINES // 2) + lin,
                        ((curses.COLS - len(m_minado[lin])) // 2) + col,
                        " ",
                    )

        rodape = "aperte qualquer tecla para iniciar"
        self.stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)

        self.stdscr.refresh()
        self.stdscr.getch()

    def derrota(self):
        # função que mostra a tela de derrota para o jogador
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
                color = 7 if b[i] > 15 else (6 if b[i] > 9 else (3 if b[i] > 4 else 1))

                if i < tamanho - 1:
                    y, x = int(i / largura), i % largura
                    char_index = min(b[i], len(char) - 1)
                    self.stdscr.addstr(
                        y, x, char[char_index], curses.color_pair(color) | curses.A_BOLD
                    )

            for lin in range(len(m_derrota)):
                for col in range(len(m_derrota[lin])):
                    p = m_derrota[lin][col]
                    y_texto = (altura // 2) - 7 + lin
                    x_texto = ((largura - len(m_derrota[lin])) // 2) + col
                    if p == 1:
                        self.stdscr.addstr(y_texto, x_texto, " ", curses.A_REVERSE)
            rodape = "aperte qualquer tecla para voltar para o menu..."
            self.stdscr.addstr(
                altura - 3, (largura - len(rodape)) // 2, rodape, curses.A_REVERSE
            )

            self.stdscr.refresh()
            if self.stdscr.getch() != -1:
                break

        self.stdscr.nodelay(False)
        self.stdscr.timeout(-1)
        self.stdscr.clear()
        self.stdscr.refresh()

    def vitoria(self, tempo):
        # função que mostra a tela de vitória para o jogador
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

        balao = [
                [0,0,0,2,2,2,0,0,0],
                [0,2,2,1,2,2,2,2,0],
                [2,2,1,2,2,2,2,2,2],
                [2,2,2,2,2,2,2,2,2],
                [2,2,2,2,2,2,2,2,2],
                [0,2,2,2,2,2,2,2,0],
                [0,0,2,2,2,2,2,0,0],
                [0,0,0,2,2,2,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,1,1,0],
                [0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,1]
                ]

        self.stdscr.clear()
        for lin in range(len(m_vitoria)):
            for col in range(len(m_vitoria[lin])):
                p = m_vitoria[lin][col]
                if p == 1:
                    self.stdscr.addstr(
                        (curses.LINES // 2) - 7 + lin,
                        ((curses.COLS - len(m_vitoria[lin])) // 2) + col,
                        " ",
                        curses.A_REVERSE,
                    )
                else:
                    self.stdscr.addstr(
                        (curses.LINES // 2) - 7 + lin,
                        ((curses.COLS - len(m_vitoria[lin])) // 2) + col,
                        " ",
                    )

        for lin in range(len(balao)):
            for col in range(len(balao[lin])):
                p = balao[lin][col]
                if p == 2:
                    self.stdscr.addstr(
                        curses.LINES - len(balao) + lin,
                        4 + col,
                        " ",
                        self.magenta_preto | curses.A_REVERSE,
                    )
                elif p == 1:
                    self.stdscr.addstr(
                        curses.LINES - len(balao) + lin,
                        4 + col,
                        " ",
                        curses.A_REVERSE,
                    )

        for lin in range(len(balao)):
            for col in range(len(balao[lin])):
                p = balao[lin][col]
                if p == 2:
                    self.stdscr.addstr(
                        curses.LINES - len(balao) + lin + 2,
                        curses.COLS - len(balao[lin]) - 4 + col,
                        " ",
                        self.azul_preto | curses.A_REVERSE,
                    )
                elif p == 1:
                    self.stdscr.addstr(
                        curses.LINES - len(balao) + lin + 2,
                        curses.COLS - len(balao[lin]) - 4 + col,
                        " ",
                        curses.A_REVERSE,
                    )

        self.stdscr.addstr(
            curses.LINES // 2 + (len(m_vitoria) // 2) + 2,
            (curses.COLS - len(tempo)) // 2,
            tempo,
        )

        rodape = "aperte qualquer tecla para voltar para o menu..."
        self.stdscr.addstr(curses.LINES - 3, (curses.COLS - len(rodape)) // 2, rodape)
        self.stdscr.refresh()
        self.stdscr.getch()
