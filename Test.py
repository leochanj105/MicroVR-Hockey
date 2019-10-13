import os
from multiprocessing import Process, Pipe
import time

def output(pipe):
    for i in range(10):
        time.sleep(0.05)
        print("P1 sending")
        pipe.send(i)


if __name__ == '__main__':
    pipe = Pipe()
    p = Process(target = output, args = (pipe[0],))
    p.start()
    for i in range(10):
        time.sleep(0.05)
        print("P2 receiving")
        print(pipe[1].recv())
    p.join()



