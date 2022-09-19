from maeda.Pt100Maeda import Pt100
import time

if __name__ == "__main__":
    
    amb = Pt100(0)
    tanque = Pt100(3)
    while True:
        
        print("Temeratura camara: {}\nTempratura Tanque: {}".format(amb.temperatura_sistema, tanque.temperatura_sistema))
        time.sleep(1)