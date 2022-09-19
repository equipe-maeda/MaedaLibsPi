import time
from maeda.Pressao4a20 import Pressao4a20
from maeda.Pt100Maeda import Pt100
from maeda.Csv import Csv
from maeda.ReleCiclicoMaeda import ReleCiclico
from maeda.Config import config
from maeda.SystemFile import File
from maeda.IOSystem import InPut, OutPut

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

TEMP_CAMARA_AMB = 20
TEMP_CAMARA_QUENTE = 100#148
TEMP_CAMARA_FRIO = -10

TEMP_TANQUE_AMB = 20
TEMP_TANQUE_1 = 93
TEMP_TANQUE_2 = 117
TEMP_TANQUE_3 = 23
TEMP_TANQUE_4 = -10

ESTAGIO_1 = 0
ESTAGIO_2 = 1
ESTAGIO_3 = 2
ESTAGIO_4 = 3

TEMPO_1 = 7200
TEMPO_2 = 3900
TEMPO_3 = 4200

TQ_H = 0
TQ_L = 1

estagios = ESTAGIO_1

ERRO_PRESS = 0.0#-2.4
pin_in_enable = InPut(input = 13) #Pin(6, Pin.IN, Pin.PULL_UP)
pin_out_valvula = 19
pin_out_temp_tanque = OutPut(16) #Pin(10, Pin.OUT)

tempo_primeira_temperatura = TEMPO_1 #7200 segundos  =  120minutos
tempo_segunda_temperatura = TEMPO_2 #3900 segundos  =  65minutos
tempo_terceira_temperatura = TEMPO_3

habilita_contagem = False

def control_temperature(estagios,
                        habilita_contagem,
                        tempo_primeira_temperatura,
                        tempo_segunda_temperatura,
                        tempo_terceira_temperatura
                        ):
    pass

        
if __name__ == "__main__":
    
#     i2c = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)
#     lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS) 
    test_canal_0 = Pressao4a20(channel = 1, erro=ERRO_PRESS)
    t_amb = Pt100(2)
    t_tanque = Pt100(3)
    
    print(habilita_contagem)
        
    csv = Csv(labels = ['Data','Hora', 'Pressao', 'Temperatura Ambiente', 'Temperatura Tanque'], directory = "dados_hba.csv")
    valvula_solenoide = ReleCiclico(base=config.BASE_TIME_SECONDS,
                                    value_ton=1,
                                    value_toff=2,
                                    start_direction = config.DIRECTION_TON,
                                    qtd_ciclos=6000,
                                    pin=pin_out_valvula,
                                    logic_state = config.LOGIC_STATE_DOW
                                    )
    
    file_ = File("config.txt")
    
    if file_:
        try:
            config = file_.read_file()
            result = config.split(';')
            estagios = int(result[0])
            habilita_contagem = int(result[1])
            habilita_contagem = bool(habilita_contagem)
            tempo_primeira_temperatura = int(result[2])
            tempo_segunda_temperatura = int(result[3])
            tempo_terceira_temperatura = int(result[4])
        except:
            print("Não há configurações para essa processo!!.")
            
    print(habilita_contagem)
    
    
    while True:
        time_loc = time.localtime()
#         print("{PP:>0.1f}".format(PP=test_canal_0.pressao_sistema))
        
#         lcd.putstr_posi(0,1,string="Pressao: {PP:>0.1f} bar  ".format(PP=abs(test_canal_0.pressao_sistema)))
        print("Pressao: {PP:>0.1f} bar  ".format(PP=abs(test_canal_0.pressao_sistema)))
#         lcd.putstr_posi(0,2,string="Ambiente: {TA:>0.1f} C  ".format(TA=t_amb.temperatura_sistema))
        print("Ambiente: {TA:>0.1f} C  ".format(TA=t_amb.temperatura_sistema))
#         lcd.putstr_posi(0,3,string="Tanque: {TT:>0.1f} C  ".format(TT=t_tanque.temperatura_sistema))
        print("Tanque: {TT:>0.1f} C  ".format(TT=t_tanque.temperatura_sistema))
        
        if pin_in_enable.input == 0:
            print("Gravando....")
###################################################################################################
            if estagios == ESTAGIO_1:
                if t_amb.temperatura_sistema >= TEMP_CAMARA_AMB:
                    print("estagio 1")
                    if t_tanque.temperatura_sistema < TEMP_TANQUE_1:
                        pin_out_temp_tanque.output(TQ_H)
                    else:
                        pin_out_temp_tanque.output(TQ_L)
                        habilita_contagem = True
                        
                    if habilita_contagem == True:
                        tempo_primeira_temperatura -= 1
                        print(tempo_primeira_temperatura)
                    
                    if tempo_primeira_temperatura <= 0:
                        tempo_primeira_temperatura = TEMPO_1
                        estagios = ESTAGIO_2
                        habilita_contagem = False
            
            elif estagios == ESTAGIO_2:
                if t_amb.temperatura_sistema >= TEMP_CAMARA_QUENTE:
                    print("estagio 2")
                    if t_tanque.temperatura_sistema < TEMP_TANQUE_2:
                        pin_out_temp_tanque.output(TQ_H)
                    else:
                        pin_out_temp_tanque.output(TQ_L)
                        habilita_contagem = True
                        
                    if habilita_contagem == True:
                        tempo_segunda_temperatura -= 1
                    
                    if tempo_primeira_temperatura <= 0:
                        tempo_segunda_temperatura = TEMPO_2
                        estagios = ESTAGIO_3
                        habilita_contagem = False

            elif estagios == ESTAGIO_3:
                print("estagio 3")
                if t_amb.temperatura_sistema <= TEMP_CAMARA_AMB:
                    if t_tanque.temperatura_sistema > TEMP_TANQUE_3:
                        pin_out_temp_tanque.output(TQ_L)
                    else:
                        habilita_contagem = True
                        
                    if habilita_contagem == True:
                        tempo_terceira_temperatura -= 1
                    
                    if tempo_primeira_temperatura <= 0:
                        tempo_terceira_temperatura = TEMPO_3
                        estagios = ESTAGIO_1
                        habilita_contagem = False
            else:
                pin_out_temp_tanque.output(TQ_L)
                print("Fim de estágio")
###################################################################################################
                
            csv.load_value(["{day:>02d}/{month:>02d}/{year:>02d}".format(day=time_loc[0], month=time_loc[1], year=time_loc[2]),
                            "{HH:>02d}:{MM:>02d}:{SS:>02d}".format(HH=time_loc[3],MM=time_loc[4],SS=time_loc[5]),
                            "{PP:>0.1f}".format(PP=abs(test_canal_0.pressao_sistema)),
                            "{TA:>0.1f}".format(TA=t_amb.temperatura_sistema),
                            "{TT:>0.1f}".format(TT=t_tanque.temperatura_sistema)
                            ])
            file_ = File("config.txt")
            file_.write_file("{a:>01d};{b:>01d};{c:>01d};{d:>01d};{e:>01d}".format(a=estagios,
                                                 b=habilita_contagem,
                                                 c=tempo_primeira_temperatura,
                                                 d=tempo_segunda_temperatura,
                                                 e=tempo_terceira_temperatura
                                                 ))
            
            
            if (estagios == ESTAGIO_1) and (t_amb.temperatura_sistema >= TEMP_CAMARA_QUENTE):
                valvula_solenoide.start()
            elif (estagios == ESTAGIO_3) and (t_amb.temperatura_sistema >= TEMP_CAMARA_FRIO):
                valvula_solenoide.pause()
            
        else:
            valvula_solenoide._pause()
            pin_out_temp_tanque.output(TQ_L)
        
        time.sleep(1)
