import math
import time
from maeda.SystemFile import File
from maeda.ADS1115 import ADS1115
from maeda.Canais import Canais


'''
Sensor de pressao 0 a 10bar:

P    -    I
0    -    4ma
10   -    20ma
'''
'''
Sensor de pressao 0 a 50bar:

P    -    I
0    -    4ma
50   -    20ma
'''

class Pressao4a20:
    def __init__(self, channel = 0, qtd_channel = 8, is_channel = False, erro = 0.0):
        self.V0 = 0
        self.V1 = 0
        self.G0 = 0.0
        self.G1 = 0.0
        self.canal = channel
        self.is_channel = is_channel
        self.erro = erro
        self.dir_dado_canal = ""
        self.class_canais = Canais(qtd_canais = qtd_channel)
        
        self._pressao_sistema = 0.0
        self.adc_1115 = 0
        
        self._set_config()
        
    @property
    def pressao_sistema(self):
        self._pressao_sistema = self.pressao()
        return self._pressao_sistema + self.erro
        
    def _set_config(self):
        
        if self.canal == 0:
           self.dir_dado_canal = "./maeda/pressao4a20/ADC0.txt"
        elif self.canal == 1:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC1.txt"
        elif self.canal == 2:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC2.txt"
        elif self.canal == 3:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC3.txt"
        elif self.canal == 4:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC4.txt"
        elif self.canal == 5:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC5.txt"
        elif self.canal == 6:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC6.txt"
        elif self.canal == 7:
            self.dir_dado_canal = "./maeda/pressao4a20/ADC7.txt"
        
        if self.is_channel == False:
            self.adc_1115 = ADS1115(channel=self.canal)
        else:
            self.adc_1115 = ADS1115(0)
            
        file = File(self.dir_dado_canal)
        if file:
            try:
                valor = file.read_file()
                result = valor.split(';')
                self.V0 = int(result[0])
                self.V1 = int(result[1])
                self.G0 = float(result[2])
                self.G1 = float(result[3])
                print(self.V0)
                print(self.V1)
                print(self.G0)
                print(self.G1)
            except:
                print("Não há configurações para canal {}.".format(self.canal))
    
    def _read_value(self):
        if self.is_channel == True:
            self.class_canais.switch_canal(self.canal)
        return self.adc_1115.readValueFrom()
            
            
    def calibracao(self):
        var = ""
        
        while var != "q":
            g0 = 0.0
            g1 = 0.0
            v0 = 0
            v1 = 0
            
            g0 = float(input("Entre com G0 do canal {}\n".format(self.canal)))
            v0 = self._read_value()
            print("V0 = {} e G0 = {}\n".format(v0, g0))
            
            g1 = float(input("Entre com G1 do canal {}\n".format(self.canal)))
            v1 = self._read_value()
            print("V1 = {} e G1 = {}\n".format(v1, g1))
            
            var = input("Digitar:\n'q' para sair sem salvar.\n's' para salvar e sair.\n'c' para configurar de novo.\n")
        
            if var == 's':
                file = File(self.dir_dado_canal)
                file.write_file("{};{};{};{}".format(v0, v1, g0, g1))
                self.V0 = v0
                self.V1 = v1
                self.G0 = g0
                self.G1 = g1
                print("Dados salvos para canal {}!".format(self.canal) )
                var = 'q'
            
        
    def pressao(self):
        a=0.0
        b=0.0
        c=0.0
        Val_x=0.0
        Gr_y=0.0
        
        if (self.V0 != self.V1) and (self.G0 != self.G1):
            a = (-self.G0+self.G1)/(-self.V0+self.V1)
            b = self.G1 - (self.V1*a)
            Val_x = self._read_value()
            Gr_y = (Val_x * a) + b
        return round(Gr_y,1)
    
            


