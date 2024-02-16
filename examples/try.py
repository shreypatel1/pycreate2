import time

try:
    while True:
        print('starting ...')
        time.sleep(1)
except KeyboardInterrupt:
    print('shutting down ... bye')
    time.sleep(0.1)