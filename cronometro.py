import time
import threading

class Cronometro:
    def __init__(self):
        self.tempo = 0
        self.thread = None
        self.cronometrando = False

    def iniciar(self):
        if not self.cronometrando:
            self.cronometrando = True
            self.thread = threading.Thread(target = self.contar, daemon = True)
            self.thread.start()

    def parar(self):
        self.cronometrando = False

    def contar(self):
        while self.cronometrando:
            time.sleep(1)
            self.tempo += 1
