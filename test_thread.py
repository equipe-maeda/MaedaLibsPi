from threading import Thread
import time

# -----

# def my_function(name, counter):
#     for x in range(counter):
#         print(name, x)
#         time.sleep(0.5)

# -----

class MyThread(Thread):
    def __init__(self, e=0):
        Thread.__init__(self)
        self.a = e

    def run(self):
        for x in range(10):
            print("Olá", self.a)
            time.sleep(0.5)

# -----
if __name__ == "__main__":
    e = MyThread(e=9)
    e.start()
