from maeda.Canais import Canais
from maeda.Pt100Canais import Pt100Canais
from machine import Pin
from maeda.ReleCiclicoMaeda import ReleCiclico
from maeda.Config import config
import utime

'''
Pt100:

C    -    Ohm
0    -    100
100  -    138.50
150  -    157.31

'''

pino_atv = Pin(25, Pin.OUT)
pino_out00 = Pin(3, Pin.OUT)
pino_out01 = Pin(4, Pin.OUT)
pino_out02 = Pin(5, Pin.OUT)

pino_in00 = Pin(7, Pin.IN)

pino_atv.value(0)
pino_out00.value(0)
pino_out01.value(0)
pino_out02.value(0)

qtd_canais = 4
qtd_ciclos = 4
valor_tempe = [0,0,0,0]

tempe_controle = 80
tempe_peca = 100

rele = ReleCiclico(base=config.BASE_TIME_MINUTES, value_ton=180, value_toff=30, qtd_ciclos=qtd_ciclos)
#rele = ReleCiclico(base=config.BASE_TIME_SECONDS, value_ton=5, value_toff=5, qtd_ciclos=qtd_ciclos)


cn = Canais(qtd_canais=qtd_canais)

pt0 = Pt100Canais(0, cn)
pt1 = Pt100Canais(1, cn)
pt2 = Pt100Canais(2, cn)
pt_ambiente = Pt100Canais(3, cn)

#pt1.calibracao()
def carrega_tempe():
    valor_tempe[0] = pt0.temperatura()
    valor_tempe[1] = pt1.temperatura()
    valor_tempe[2] = pt2.temperatura()
    valor_tempe[3] = pt_ambiente.temperatura()

def desliga_saidas():
    pino_out00.value(0)
    pino_out01.value(0)
    pino_out02.value(0)
    
def controla_saidas():
    if valor_tempe[0] <= tempe_peca:
        pino_out00.value(1)
    else:
        pino_out00.value(0)
    
    if valor_tempe[1] <= tempe_peca:
        pino_out01.value(1)
    else:
        pino_out01.value(0)
        
    if valor_tempe[2] <= tempe_peca:
        pino_out02.value(1)
    else:
        pino_out02.value(0)
        
    print("Temperatura Ambiente: {}\nPeça 1: {}\nPeça 2: {}\nPeça 3: {}\nCiclo nº: {}\n".format(valor_tempe[3], valor_tempe[0], valor_tempe[1], valor_tempe[2], rele.cnt_ciclos))

while True:
    if pino_in00.value() == 0:
        rele.start()
        if (valor_tempe[3] >= tempe_controle) and (rele.out_internal == 1):
            controla_saidas()
        elif valor_tempe[3] < tempe_controle:
            print("Aguardando temperatura ambiente chegar a {} graus.\nValor atual: {} graus".format(tempe_controle,valor_tempe[3]))
        elif ((rele.out_internal == 0) and (rele.cnt_ciclos <= qtd_ciclos)):
            print("Aguardando tempe de desligamento: {} seg de {} seg".format(rele.cnt_toff,rele.value_toff*60))
            if rele.cnt_ciclos >= qtd_ciclos:
                while True:
                    desliga_saidas()
                    print("Fim de ciclo\nFavor desligar equipamento para reiniciar novamente\n")
                    utime.sleep(4)
        
        pino_atv.toggle()
        utime.sleep(0.5)
    else:
        rele.pause()
        desliga_saidas()
    pino_atv.toggle()
    carrega_tempe()
    utime.sleep(0.5)
