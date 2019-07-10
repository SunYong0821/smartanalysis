from multiprocessing import Pool, RLock
from time import sleep
from datetime import datetime

rl = RLock()

def test(i):
    print(i)
    rl.acquire()
    with open('test.txt', 'a') as out:
        out.write(f'{i} is doing...\n')
    rl.release()
    sleep(3)

if __name__ == '__main__':
    p = Pool(4, initargs=(rl,))
    print(datetime.now())
    for i in range(4):
        p.apply_async(test, (i,))
    p.close()
    p.join()
    print(datetime.now())