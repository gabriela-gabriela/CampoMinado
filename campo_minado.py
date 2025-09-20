import campo


def game_over():
    print("voce perdeu")
    print("veja as localizações das bombas abaixo")
    # print(c.campo_minado) tenho q ver um jeito de fazer a variavel de la passar pra ca (talvez seja uma boa criar uma classe pra aqui)


def vitoria():
    print("parabéns, você venceu")


def play():
    c = campo.Campo(5, 5, 5)
    c.criar_campos()
#    for lin in range(len(c.campo_minado)):
#        print(c.campo_minado[lin])
#    print(" ")

    casas_vazias = (c.altura * c.largura) - c.n_bombas
    while True:
        for lin in range(len(c.campo_de_jogo)):
            print(c.campo_de_jogo[lin])

        while True:
            tipo_jogada = input("cavar(c) ou marcar(m)? ")
            if tipo_jogada == "c":
                jogada_lin, jogada_col = input("jogada? '{linha} {coluna}' ").split() #tem q fazer um try except aqui

                if c.campo_minado[int(jogada_lin)][int(jogada_col)] == "*":
                    return game_over()

                casas_cavadas = c.cavar(int(jogada_lin), int(jogada_col), 0)

                if casas_cavadas == "gameover":
                    return game_over()

                casas_vazias -= casas_cavadas
#                print(f"casas que supostamente faltam cavar: {casas_vazias}")

                if casas_vazias == 0:
                    return vitoria()
                break

            elif tipo_jogada == "m":
                jogada_lin, jogada_col = input("jogada? '{linha} {coluna}' ").split()
                c.marcar_bomba(int(jogada_lin), int(jogada_col))
                break

            else:
                print("tipo de jogada inválido, tente novamente:")


play()
