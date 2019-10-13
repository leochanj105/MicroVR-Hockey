from ContinuousGesturePredictor import *
import time
import multiprocessing
from ball_tracking import *


if __name__ == "__main__": 
	
    parent_conn, child_conn = multiprocessing.Pipe()

    # creating new processes

    p1 = multiprocessing.Process(target=main_a, args=(parent_conn,))
    # running processes
    p1.start()

    # wait until processes finish 
    p1.join()
	

