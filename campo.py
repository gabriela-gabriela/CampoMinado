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

    def plantar_bombas(self, y, x):
        bombas_plantadas = 0
        while bombas_plantadas < self.n_bombas:
            locx = random.randint(0, self.largura - 1)
            locy = random.randint(0, self.altura - 1)

            if self.campo_minado[locy][locx] == None and (locx, locy) not in [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]: # esse list comprehension cria uma lista com os vizinhos de x, y
                self.campo_minado[locy][locx] = "*"
                bombas_plantadas += 1

    def contar_bombas_vizinhas(self, y, x, bomba=None):
        # se a bomba for None ele vai contar as bombas reais ao redor, se for x, ele vai contar as bombas marcadas ao redor
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
        # funcao para trocar os valores da matriz pelo numero de bombas ao redor
        for lin in range(self.altura):
            for col in range(self.largura):
                if self.campo_minado[lin][col] != "*":
                    self.campo_minado[lin][col] = str(
                        self.contar_bombas_vizinhas(lin, col)
                    )

    def criar_campos(self, y, x):
        self.plantar_bombas(y, x)
        self.numerar_bombas_vizinhas()

    def cavar(self, y, x):
        # essa funcao aqui vai retornar o numero de casas cavadas ou "gameover" caso uma bomba seja cavada
        cavadas = 0
        if self.matriz_foi_cavada[y][x]:
            cavadas = self.cavar_por_numero(y, x, cavadas)

        else:
            cavadas = self.cavar_nao_cavadas(y, x, cavadas)

        return cavadas

    def cavar_nao_cavadas(self, y, x, cavadas):
        if self.matriz_foi_cavada[y][x]:
            return 0

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
                            cavadas += self.cavar_nao_cavadas(lin, col, 0)

        else:
            self.campo_de_jogo[y][x] = self.campo_minado[y][x]
            self.matriz_foi_cavada[y][x] = True
            cavadas = 1

        return cavadas

    def cavar_por_numero(self, y, x, cavadas):
        if (
            self.campo_de_jogo[y][x].isdigit()
            and 0 < int(self.campo_de_jogo[y][x]) < 9
            and self.matriz_verificacao[y][x]
            ):
            bombas_marcadas_ao_redor = self.contar_bombas_vizinhas(y, x, "x")
            if int(self.campo_de_jogo[y][x]) == bombas_marcadas_ao_redor:
                self.matriz_verificacao[y][x] = False
                for lin in range(y - 1, y + 2):
                    if 0 <= lin < self.altura:
                        for col in range(x - 1, x + 2):
                            if 0 <= col < self.largura:
                                resultado = self.cavar_nao_cavadas(lin, col, 0)
                                if resultado == "gameover":
                                    return "gameover" #se eu colocar a funcao de game over aqui ou criar um novo arquivo pra ela eu acho q fica melhor
                                cavadas += resultado
            return cavadas


    def marcar_bomba(
        self, y, x
        ):
        if self.campo_de_jogo[y][x] == "x":
            self.campo_de_jogo[y][x] = "o"
        elif self.campo_de_jogo[y][x] == "o":
            self.campo_de_jogo[y][x] = "x"
        else:
            pass
