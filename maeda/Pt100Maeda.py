import math
import time
from maeda.SystemFile import File
from maeda.ADS1115 import ADS1115
from maeda.Canais import Canais

'''
Pt100:

C    -    Ohm
-50  -    80.31
-20  -    92.16
0    -    100
100  -    138.50
150  -    157.31

'''

class Pt100:
    def __init__(self, canal, qtd_channel = 8, is_channel = False):

        self.V0 = 0
        self.V1 = 0
        self.G0 = 0.0
        self.G1 = 0.0
        self.canal = canal
        self.class_canais = Canais(qtd_canais = qtd_channel)
        self.dir_dado_canal = ""
        self.is_channel = is_channel
        
        self.range_temp_positivo = 99.22 # Resistencia do Pt100 a -2 graus ceusius
        
        self._temperatura_sistema = 0.0
        
        self._set_config()
        self.adc_1115 = ADS1115(channel=self.canal)
    
    @property
    def temperatura_sistema(self):
        self._temperatura_sistema = self.temperatura()
        return self._temperatura_sistema
            
    def _set_config(self):
        
        if self.canal == 0:
           self.dir_dado_canal = "./maeda/pt100/ADC0.txt"
        elif self.canal == 1:
            self.dir_dado_canal = "./maeda/pt100/ADC1.txt"
        elif self.canal == 2:
            self.dir_dado_canal = "./maeda/pt100/ADC2.txt"
        elif self.canal == 3:
            self.dir_dado_canal = "./maeda/pt100/ADC3.txt"
        elif self.canal == 4:
            self.dir_dado_canal = "./maeda/pt100/ADC4.txt"
        elif self.canal == 5:
            self.dir_dado_canal = "./maeda/pt100/ADC5.txt"
        elif self.canal == 6:
            self.dir_dado_canal = "./maeda/pt100/ADC6.txt"
        elif self.canal == 7:
            self.dir_dado_canal = "./maeda/pt100/ADC7.txt"
            
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
                print("Não há configurações.")
            
            
    def calibracao(self):
        var = ""
        
        while var != "q":
            g0 = 0.0
            g1 = 0.0
            v0 = 0
            v1 = 0
            
            g0 = float(input("Entre com G0\n"))
            v0 = self._get_ad()
            print("V0 = {} e G0 = {}\n".format(v0, g0))
            
            g1 = float(input("Entre com G1\n"))
            v1 = self._get_ad()
            print("V1 = {} e G1 = {}\n".format(v1, g1))
            
            var = input("Digitar:\n'q' para sair sem salvar.\n's' para salvar e sair.\n'c' para configurar de novo.\n")
        
            if var == 's':
                file = File(self.dir_dado_canal)
                file.write_file("{};{};{};{}".format(v0, v1, g0, g1))
                self.V0 = v0
                self.V1 = v1
                self.G0 = g0
                self.G1 = g1
                print("Dados salvos!" )
                var = 'q'
            
        
    def temperatura(self):
        razao_1=0.0
        razao_2=0.0
        Val_x=0.0
        Gr_y=0.0
        
        R=0;
        Pt=100;
        a= -0.580195 * pow(10,-6)
        b= 3.90802 * pow(10,-3)
        c = 0.0
        t=0;
        
        if (self.V0 != self.V1) and (self.G0 != self.G1):
            razao_1 = (self.G1-self.G0)/(self.V1-self.V0)
            razao_2 = self.G1 - (self.V1*razao_1)
            Val_x = self.adc_1115.readValueFrom()
        
            Gr_y = (Val_x * razao_1) + razao_2
#             Gr_y = 96.09#97.65 #98.83
            
        if Gr_y > self.range_temp_positivo:
            
            R = Gr_y
            c = 1-(R/Pt)
            
            sq = pow(b,2)-(4*(a)*c)
            t = ( -b + math.sqrt( sq ) )/(2*a)
            Gr_y = t
        else:
            R = Gr_y
            a_ = (-(-4.2735))*pow(10,-12)*100
            b_ = (-0.580195)*pow(10,-6)
            c_ = ( (-4.2735)*pow(10,-12) ) + ( 3.90802*pow(10, -3) )
            d_ = 1-(R/Pt)
            q_ = ( 2*pow(b_, 3) - 9*a_*b_*c_ + 27*pow(a_, 2)*d_ ) / (27*pow(a_, 3))
            p_ = ( (-pow(b_, 2)) / (3*pow(a_, 2)) ) + ( c_/a_ )
            
            sq = (pow(q_, 2)/4 + pow(p_, 3)/27)
            
            t = ( self.cubic_root( -(q_/2) + math.sqrt(sq) ) ) + ( self.cubic_root( -(q_/2) - math.sqrt(sq) ) - (b_/(3*a_)) )
            Gr_y = t
            
        
        return round(Gr_y,1)
    
    def cubic_root(self, x):
        ret = 0
        if x < 0:
            x = abs(x)
            ret = x ** (1/3) * (-1)
        else:
            ret = x ** (1/3)
        
        return round(ret)
        
            
    def _get_ad(self):
        
        if self.is_channel == True:
            self.class_canais.switch_canal(self.canal)
        analog_value = self.adc_1115.readValueFrom()   
        return analog_value
    
if __name__ == "__main__":
    
    amb = Pt100(2)
    tanque = Pt100(3)
    while True:
        
        print("Temeratura camara: {}\nTempratura Tanque: {}".format(amb.temperatura_sistema, tanque.temperatura_sistema))
        time.sleep(1)

            
