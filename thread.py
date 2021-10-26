from concurrent.futures import ThreadPoolExecutor
from time import sleep
from chat import Session
import threading
import random
import queue
import time

class DESchat():
    def __init__(self):
        DESchat.check = False
        pass
    
    def getChat(self):
        while True:
            if DESchat.check:
                break
            time.sleep(4)
            
    def startThread(self,DESchat):
        thread = myThread()
        thread.start()
        return thread

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        DESchat.getChat(self,DESchat)

if __name__ == '__main__':
    pass