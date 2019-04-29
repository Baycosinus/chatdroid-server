import sys
import socket
import db
from threading import Thread
import json


HOST = "192.168.1.6"
TARGET = "0.0.0.0"
PORT = 8888
RESPONSE = ""

def listen():
    global TARGET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Port dinleniyor.")
        print("IP: " + HOST)
        print("PORT: " + str(PORT))
        sock.bind((HOST, PORT))
        sock.listen(10)
        while 1:
            conn, addr = sock.accept()
            TARGET = addr[0]
            buf = conn.recv(1024)
            msg = buf.decode()
            # msg = json.loads(msg)
            process(addr[0], msg)
    except Exception as e:
        print('Listen Error: ' + str(e)) 
        sys.exit()


def send():
    global TARGET
    global RESPONSE
    print("Target: " + str(TARGET))
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET, PORT))
        sock.sendto(RESPONSE.encode(), (TARGET, PORT))
        print("Message: " + RESPONSE)
        sock.close()
    except Exception as e:
        print("Send Error: " + str(e))
        sys.exit()

def process(addr, msg):
    global RESPONSE
    print(addr + ":" + msg)
    # Load JSON here instead of splitting the text.
    hash = msg.split(':')
    command = hash[0]

    if (command == "Register"):
        username = hash[1]
        password = hash[2]
        db.register(username,password)
    elif (command == "CheckAvailable"):
        username = hash[1]
        RESPONSE = str(db.check_available(username))
        sthread = Thread(target=send)
        sthread.start()
        sthread.join()
    elif (command == "Login"):
        username = hash[1]
        password = hash[2]
        ip = addr[0]
        RESPONSE = db.login(username,password,ip)
        sthread = Thread(target = send)
        sthread.start()
        sthread.join()
    return 0
    
if __name__ == '__main__':
    # listen() fonksiyonu için bir thread hazırladık.
    lthread = Thread(target=listen)
    # send() fonksiyonu için bir thread hazırladık.
    #sthread = Thread(target=send)

    lthread.start()  # threadleri başlatıyoruz.
    #sthread.start()  # ''

    lthread.join()  # threadleri ana thread'e (main fonksiyonuna bağlıyoruz)
    #sthread.join()  # böylece listen ve send threadleri sonlanmadan ana thread kapanmıyor. BİZ BİTTİ DEMEDEN BİTMEZ AGA!
