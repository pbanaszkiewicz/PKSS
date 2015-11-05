# coding: utf-8
import time

import zmq


if __name__ == "__main__":
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)

    # time synchronization source
    subscriber.connect("tcp://192.168.0.50:5563")

    # helpful when you run the time_server.py locally
    subscriber.connect("tcp://localhost:5563")

    # messages send from the time source
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time_speedup")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time")

    # if you want to receive messages from other sources too:
    subscriber.connect("tcp://192.168.0.51:5563")  # MPEC
    subscriber.setsockopt(zmq.SUBSCRIBE, b"awaria")

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
