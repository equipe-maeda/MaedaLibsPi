from maeda.IOSystem import OutPut

class Canais:
    def __init__(self, qtd_canais = 8, pino_c0 = 40, pino_c1 = 16, pino_c2 = 15 ):
        self.pino_c0 = OutPut(pino_c0)
        self.pino_c1 = OutPut(pino_c1)
        self.pino_c2 = OutPut(pino_c2)
        
        self.valor_ad = []
        self.qtd_canais = qtd_canais
        self.index_canais = 0
        
    def switch_canal(self, canal):
        if canal == 0:
            self.pino_c0.output(0)
            self.pino_c0.output(0)
            self.pino_c0.output(0)
            
        elif canal == 1:
            self.pino_c0.output(1)
            self.pino_c0.output(0)
            self.pino_c0.output(0)
        elif canal == 2:
            self.pino_c0.output(0)
            self.pino_c0.output(1)
            self.pino_c0.output(0)
        elif canal == 3:
            self.pino_c0.output(1)
            self.pino_c0.output(2)
            self.pino_c0.output(0)
        elif canal == 4:
            self.pino_c0.output(0)
            self.pino_c0.output(0)
            self.pino_c0.output(1)
        elif canal == 5:
            self.pino_c0.output(1)
            self.pino_c0.output(0)
            self.pino_c0.output(1)
        elif canal == 6:
            self.pino_c0.output(0)
            self.pino_c0.output(1)
            self.pino_c0.output(2)
        elif canal == 7:
            self.pino_c0.output(1)
            self.pino_c0.output(1)
            self.pino_c0.output(1)
    