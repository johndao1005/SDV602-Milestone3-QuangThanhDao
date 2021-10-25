from concurrent.futures import ThreadPoolExecutor
from time import sleep


def threads(username):
    from view.dataView import dataView
    mainDES = dataView(username)
    executor = ThreadPoolExecutor(4)
    thread1 = executor.submit(mainDES.mainloop,)
    sleep(0.5)
    thread2 = executor.submit(print,'Hello')
    print("Thread 1 executed ? :",thread1.done())
    print("Thread 2 executed ? :",thread2.done())