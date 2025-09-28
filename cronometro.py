import time
import threading
# uso do threading pois a contagem do tempo tem que ser feita paralelamente ao funcionamento do jogo


class Cronometro:
    def __init__(self):
        self.tempo = 0
        self.thread = None
        self.cronometrando = False

    def iniciar(self):
        # função que inicia o cronômetro caso a contagem ainda não tenha sido iniciada
        if not self.cronometrando:
            self.cronometrando = True
            self.thread = threading.Thread(target=self.contar, daemon=True)
            self.thread.start()

    def parar(self):
        # função que para o cronômetro
        self.cronometrando = False

    def contar(self):
        # função que faz o cronômetro funcionar e aumentar o tempo a casa segundo
        while self.cronometrando:
            time.sleep(1)
            self.tempo += 1
