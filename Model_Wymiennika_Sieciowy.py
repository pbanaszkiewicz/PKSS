# coding: utf-8
import datetime
import time
import sys
import zmq

def Wymiennik(Fzm, Tzm, Tpco, Tpm, Tzco):
    Tpm_next = (Fzm*s*Cw*(Tzm-Tpm)-Kw*(Tpm-Tzco))/(Mm*Cwym) + Tpm
    Tzco_next = (-Fzco*s*Cw*(Tzco-Tpco)+Kw*(Tpm-Tzco))/(Mco*Cwym) + Tzco

    return Tpm_next, Tzco_next

# stale
Mm = 3000.0
Mco = 3000.0
Cwym = 2700.0
s = 1000.0
Cw = 4200.0
Kw = 250000.0
Fzco = 150.0/3600

# zmienne zewnetrzne (pobierane z serwera)
f_zm = 30.0/3600
t_zm = 90.0
t_pco = 40.0

# punkty startowe
t_pm = 90.0
t_zco = 20.0

if __name__ == "__main__":
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp:192.168.0.52:5563")
    
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://192.168.0.50:5563")
    subscriber.connect("tcp://192.168.0.51:5563")
    subscriber.connect("tcp://192.168.0.53:5563")
    subscriber.connect("tcp://192.168.0.54:5563")
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time_speedup")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"time")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"t_zm")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"f_zm")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"t_pco")

    time_speedup = 1

    while True:
        try:
            address, content = subscriber.recv_multipart()
            address = address.decode('utf-8')
            content = content.decode('utf-8')

            if address == "time_speedup":
                time_speedup = int(content)
            elif address == "t_zm":
                t_zm = float(content)
            elif address == "f_zm":
                f_zm = float(content)
            elif address == "t_pco":
                t_pco = float(content)
            elif address == "time":
                t_pm, t_zco = Wymiennik(f_zm, t_zm, t_pco, t_pm, t_zco)
                publisher.send_multipart([
                    b"t_pm",
                    "{}".format(t_pm).encode("utf-8"),
                ], zmq.NOBLOCK)
                publisher.send_multipart([
                    b"t_zco",
                    "{}".format(t_zco).encode("utf-8"),
                ], zmq.NOBLOCK)

            print("[{}] {}".format(address, content))

        except KeyboardInterrupt:
            print("Terminating")
            subscriber.close()
            publisher.close()
            ctx.term()
            break

