from ContinuousGesturePredictor import *
import time
import multiprocessing
  
# def sender(y): 
#     """ 
#     function to send messages to other end of pipe 
#     """
#     sleep(0.01)
#     predict_main()
#     y.send(predictedClass)
#     print("Sent the message: {}".format(predictedClass))

# def receiver(x):
# 	out = x.recv()
# 	print("Received the message: {}".format(out))

if __name__ == "__main__": 
	print("1")
    # creating a pipe 
	parent_conn, child_conn = multiprocessing.Pipe()

    # creating new processes 

	p1 = multiprocessing.Process(target=detector, args=(parent_conn,)) 
	p1.start()
	while(True):
		time.sleep(0.001)
		msg = child_conn.recv()
		if(msg == "OVER"):
			exit(0)
		print(msg)
    
    # running processes 
	 
	 

    # wait until processes finish 
	p1.join() 
	

