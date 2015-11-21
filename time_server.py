# coding: utf-8
import time
import sys

import zmq


if __name__ == "__main__":
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:5563")

    time_speedup = 30
    runtime = 0

    while True:
        try:
            publisher.send_multipart([
                b"time_speedup",
                "{}".format(time_speedup).encode("utf-8"),
            ], zmq.NOBLOCK)
            publisher.send_multipart([
                b"time",
                "{}".format(runtime).encode("utf-8"),
            ], zmq.NOBLOCK)

            runtime += 1
            time.sleep(1 / time_speedup)

        except KeyboardInterrupt:
            print("Quit [Y] or change speedup [n]? [Y/n] >>> ")
            q = input("")
            if q == "Y":
                sys.exit(0)
            else:
                time_speedup = int(input("Select time speedup: "))
                assert time_speedup > 0
