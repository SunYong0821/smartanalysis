from multiprocessing import Pool
from time import sleep
from datetime import datetime

def test(i):
    print(f'{i} is doing...')
    sleep(3)

if __name__ == '__main__':
    p = Pool(4)
    print(datetime.now())
    for i in range(4):
        p.apply_async(test, (i,))
    p.close()
    p.join()
    print(datetime.now())