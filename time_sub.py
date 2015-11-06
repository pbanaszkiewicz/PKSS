# coding: utf-8
import time

import zmq


if __name__ == "__main__":
    clock = -1

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

    # publish information about clock desynchronization
    publisher = ctx.socket(zmq.PUB)
    # different port, because 5563 is taken when you run `time_server.py`
    # locally
    publisher.bind("tcp://*:5564")

    time_speedup = 1

    while True:
        try:
            address, content = subscriber.recv_multipart()
            address = address.decode('utf-8')
            content = content.decode('utf-8')

            if address == "time_speedup":
                time_speedup = int(content)

            elif address == "time":
                clock_msg = int(content)

                # start counting when the first clock message arrives
                if clock < 0:
                    clock = clock_msg
                else:
                    clock += 1

                if abs(clock - clock_msg) >= 100:
                    # will be sent out every time there's a different between
                    # local clock and external synchronization signal (from
                    # `time_server.py`)
                    publisher.send_multipart([
                        b"awaria_sub",
                        "Awaria!!!".encode("utf-8"),
                    ], zmq.NOBLOCK)  # non-blocking: won't block the while loop

                    print("[{}] {}".format("ERROR", "Zglaszam awarie"))

            print("[{}] {}".format(address, content))
    
            time.sleep(0.5 / time_speedup)

        except KeyboardInterrupt:
            print("Terminating")
            subscriber.close()
            ctx.term()
            break
