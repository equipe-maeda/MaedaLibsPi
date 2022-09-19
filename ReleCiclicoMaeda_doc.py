'''
Classe = ReleCiclicoMaeda

Argumentos de entrada:
* base = Base de tempo a ser usado - segundos, minutos ou horas
* value_ton = Aquantidade de tempo que a saída será acionada
* value_toff = Aquantidade de tempo que a saída será desacionada
* start_direction = Define se começa com saída ligada ou desligada
* qtd_ciclos = A quantidade de ciclos que serão executados
* pin = O pino GPIO que será usado na saída

Recursos a serem usados:
* A classe config, no modulo maeda.Config:
  Dentro dessa classe estão constantes e recursos que serão usados no sistema
  
Metodos:
* start() = Inicia o relé
* 
'''

from maeda.ReleCiclicoMaeda import ReleCiclico
from maeda.Config import config
from machine import Pin
import utime

pin_out = Pin(25, Pin.OUT)
pin_in = Pin(22, Pin.IN, Pin.PULL_UP)
pin_in_reset = Pin(21, Pin.IN, Pin.PULL_UP)
rele = ReleCiclico(
                 base=config.BASE_TIME_SECONDS,
                 value_ton=2,
                 value_toff=2,
                 start_direction = config.DIRECTION_TON,
                 qtd_ciclos=2,
                 pin=pin_out,
                 logic_state = config.LOGIC_STATE_UP
                  )


while True:
    if pin_in.value() == 0:
        rele.start()
        while rele.start_cnt:
            #print("Contador: {}".format(cnt.cnt_ciclos))
            utime.sleep(1)
            if pin_in_reset.value() == 0:
                rele.stop()
                print('Contador parado')
        if rele.final_ciclo == True:
            print("Final do Ciclo")
                
        utime.sleep(1)
                