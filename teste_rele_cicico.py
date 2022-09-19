# import RPi.GPIO as GPIO
# import time
# 
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# 
# GPIO.setup(29, GPIO.OUT)
# 
# GPIO.output(29, 1)
# time.sleep(2)
# GPIO.output(29, 0)
# time.sleep(2)
from maeda.ReleCiclicoMaeda import ReleCiclico
from maeda.Config import config

# if __name__ == "__main__":

rele = ReleCiclico(
             base=config.BASE_TIME_SECONDS,
             value_ton=1,
             value_toff=1,
             start_direction = config.DIRECTION_TON,
             qtd_ciclos=6,
             pin=5,
             logic_state = config.LOGIC_STATE_UP
              )
rele.start_run()


