from maeda.Pressao4a20 import Pressao4a20
import time

if __name__ == "__main__":
#     pin_out = []
#     
#     pin_out.append(Pin(7, Pin.OUT))
#     pin_out.append(Pin(10, Pin.OUT))
#     pin_out.append(Pin(11, Pin.OUT))
#     pin_out.append(Pin(12, Pin.OUT))
    
   
    test_canal_0 = Pressao4a20(channel = 1)
    test_canal_0.calibracao()
    
#     cnt = 0
    
    while 1:
        print(test_canal_0.pressao_sistema)
#         print(cnt)
        
#         pin_out[cnt].toggle()
#         cnt += 1
#         if cnt >= len(pin_out):
#             cnt=0
        
        time.sleep(1)