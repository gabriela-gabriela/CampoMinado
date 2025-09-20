import random


class Campo:
    def __init__(self, altura, largura, n_bombas):
        self.altura = altura
        self.largura = largura
        self.n_bombas = n_bombas
        self.campo_minado = [[None for col in range(largura)] for lin in range(altura)]
        self.campo_de_jogo = [["o" for col in range(largura)] for lin in range(altura)]
        self.matriz_verificacao = [[True for col in range(largura)] for lin in range(altura)] #matriz pra evitar que vire um loop infinito
        self.matriz_foi_cavada = [[False for col in range(largura)] for lin in range(altura)]

    def plantar_bombas(self):
        bombas_plantadas = 0
        while bombas_plantadas < self.n_bombas:
            locx = random.randint(0, self.largura - 1)
            locy = random.randint(0, self.altura - 1)

            if self.campo_minado[locy][locx] == None:
                self.campo_minado[locy][locx] = "*"
                bombas_plantadas += 1

    def contar_bombas_vizinhas(self, y, x, bomba=None):
        campo = self.campo_de_jogo
        if bomba == None:
            bomba = "*"
            campo = self.campo_minado

        bombas_vizinhas = 0
        for lin in range(y - 1, y + 2):
            if lin >= 0 and lin < self.altura:
                for col in range(x - 1, x + 2):
                    if col >= 0 and col < self.largura and campo[lin][col] == bomba:
                        bombas_vizinhas += 1
        return bombas_vizinhas

    def numerar_bombas_vizinhas(self):
        for lin in range(self.altura):
            for col in range(self.largura):
                if self.campo_minado[lin][col] != "*":
                    self.campo_minado[lin][col] = str(
                        self.contar_bombas_vizinhas(lin, col)
                    )

    def criar_campos(self):
        self.plantar_bombas()
        self.numerar_bombas_vizinhas()

    def cavar(self, y, x, cavadas):
#        print(f"funcao cavar na casa: {y}, {x}")
        if self.matriz_foi_cavada[y][x]: #verifica se a casa já foi cavada (nesse caso aqui ela foi)
            print(self.matriz_verificacao)
            if (
                self.campo_de_jogo[y][x].isdigit()
                and 0 < int(self.campo_de_jogo[y][x]) < 9
                and self.matriz_verificacao[y][x]
            ):
                bombas_marcadas_ao_redor = self.contar_bombas_vizinhas(y, x, "x")
#                print(bombas_marcadas_ao_redor)
                if int(self.campo_de_jogo[y][x]) == bombas_marcadas_ao_redor:
                    self.matriz_verificacao[y][x] = False
                    for lin in range(y - 1, y + 2):
                        if 0 <= lin < self.altura:
                            for col in range(x - 1, x + 2):
                                if 0 <= col < self.largura:
                                    resultado = self.cavar(lin, col, 0)
                                    if resultado == "gameover":
                                        return "gameover" #se eu colocar a funcao de game over aqui ou criar um novo arquivo pra ela eu acho q fica melhor
                                    cavadas += resultado

        else: #se a casa ainda não tiver sido cavada
            if self.campo_de_jogo[y][x] == "x": # vc fica impedido de cavar uma loc marcada
                return 0

            if self.campo_minado[y][x] == "*":
                return "gameover"

            elif self.campo_minado[y][x] == "0":
                self.campo_de_jogo[y][x] = " "
                self.matriz_foi_cavada[y][x] = True
                cavadas += 1
                for lin in range(y - 1, y + 2):
                    if 0 <= lin < self.altura:
                        for col in range(x - 1, x + 2):
                            if 0 <= col < self.largura and (x, y) != (col, lin):
                                cavadas += self.cavar(lin, col, 0)

            else:
                self.campo_de_jogo[y][x] = self.campo_minado[y][x]
                self.matriz_foi_cavada[y][x] = True
                cavadas = 1

#        print(f"cavadas: {cavadas}")
        return cavadas

    def marcar_bomba(
        self, y, x
        ):
        if self.campo_de_jogo[y][x] == "x":
            self.campo_de_jogo[y][x] = "o"
        elif self.campo_de_jogo[y][x] == "o":
            self.campo_de_jogo[y][x] = "x"
        else:
            print("opção inválida, tente novamente")
