from ball_tracking import *
import time
import multiprocessing



if __name__ == "__main__": 
	print("1")
	# creating a pipe
	parent_conn_1, child_conn = multiprocessing.Pipe()

	# creating new processes

	p1 = multiprocessing.Process(target=main_a, args=(parent_conn_1, ))
	p1.start()
	while(True):
		time.sleep(0.001)
		result = child_conn.recv()
    
	# running processes

    # wait until processes finish 
	p1.join() 
	
