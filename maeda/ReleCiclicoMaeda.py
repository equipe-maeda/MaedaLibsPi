
# import math
import time
# from typing import Any
from maeda.Config import config
from maeda.IOSystem import OutPut
from threading import Thread
# from multiprocessing import Process

class ReleCiclico(Thread):
    def __init__(self, base = config.BASE_TIME_SECONDS, value_ton=1, value_toff=1, start_direction = config.DIRECTION_TON, qtd_ciclos = 1, pin = None, logic_state=config.LOGIC_STATE_UP):
        self.base = base
        self.value_ton = value_ton
        self.value_toff = value_toff
        self.start_direction = start_direction
        self.qtd_ciclos = qtd_ciclos
        self.out_relay = pin
        self.out_internal = False
        self.cnt_ciclos = 1
        self.start_cnt = False
        self.logic_state = logic_state
        
        self.cnt_ton = 1
        self.cnt_toff = 1
        
        self.cnt_old = self.cnt_ciclos
        self.final_ciclo = False
        self.output = None
        
        if self.out_relay != None:
            self.output = OutPut(self.out_relay)

        Thread.__init__(self)
        Thread.start(self)
        
    def start_run(self):
        if self.start_cnt == True:
            print('Relé já iniciou.')
        else:
            self.start_cnt = True
            self.final_ciclo = False
            
    def _pause(self):
        self.start_cnt = False
        self.out_relay_status(0)
        
    def _stop(self):
        self.start_cnt = False
        self.out_relay_status(0)
        self.cnt_ciclos=1
        self.cnt_ton=1
        self.cnt_toff=1
        self.cnt_old = self.cnt_ciclos
                
    def _logic_relay(self,mult):      
        if self.cnt_old == self.cnt_ciclos:
            print("Ciclo: {}".format(self.cnt_ciclos))
            self.cnt_old+=1
        
        if self.start_direction == config.DIRECTION_TON:
            if self.cnt_ton <= self.value_ton*mult:
                self.out_relay_status(1)
                self.cnt_ton+=1
                time.sleep(1)
            elif self.cnt_toff <= self.value_toff*mult:
                self.out_relay_status(0)
                self.cnt_toff+=1
                time.sleep(1)
            elif self.cnt_toff >= self.value_toff*mult:
                self.cnt_ton=1
                self.cnt_toff=1
                self.cnt_ciclos+=1
            
        elif self.start_direction == config.DIRECTION_TOFF:
            if self.cnt_toff <= self.value_toff*mult:
                self.out_relay_status(0)
                self.cnt_toff+=1
                time.sleep(1)
            elif self.cnt_ton <= self.value_ton*mult:
                self.out_relay_status(1)
                self.cnt_ton+=1
                time.sleep(1)
            elif self.cnt_ton >= self.value_ton*mult:
                self.cnt_ton=1
                self.cnt_toff=1
                self.cnt_ciclos+=1
            
        if self.cnt_ciclos > self.qtd_ciclos:
            self.cnt_ciclos=1
            self.cnt_old = self.cnt_ciclos
            self.start_cnt = False
            self.cnt_ton=1
            self.cnt_toff=1
            self.final_ciclo = True
                        
    def out_relay_status(self, value):
        if self.out_relay == None:
            self.out_internal = value
        else:
            if self.logic_state == config.LOGIC_STATE_UP:
                self.output.output(value)
            else:
                v = not value
                self.output.output(v)
                
    def run(self):
        print('Entrou na thread')
        while True:
            if self.start_cnt == True:
                if self.base == config.BASE_TIME_SECONDS:
                    self._logic_relay(1)
                elif self.base == config.BASE_TIME_MINUTES:
                    self._logic_relay(60)
                elif self.base == config.BASE_TIME_HOURS:
                    self._logic_relay(120)
                else:
                    time.sleep(1)
            else:
                time.sleep(1)
                
if __name__ == "__main__":
    rele = ReleCiclico(base = config.BASE_TIME_SECONDS,
                       value_ton=1,
                       value_toff=1,
                       start_direction = config.DIRECTION_TON,
                       qtd_ciclos = 3,
                       pin = 29,
                       logic_state=config.LOGIC_STATE_DOW)
    rele.start_run()
