# coding: utf-8
import time

import zmq


if __name__ == "__main__":
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://192.168.0.50:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time_speedup")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time")

    time_speedup = 1

    while True:
        try:
            address, content = subscriber.recv_multipart()
            address = address.decode('utf-8')
            content = content.decode('utf-8')

            if address == "time_speedup":
                time_speedup = int(content)

            print("[{}] {}".format(address, content))
    
            time.sleep(0.5 / time_speedup)

        except KeyboardInterrupt:
            print("Terminating")
            subscriber.close()
            ctx.term()
            break
