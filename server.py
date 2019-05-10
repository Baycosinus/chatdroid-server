import sys, os
import socket
import db
from threading import Thread
import json


HOST = "192.168.1.105"
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
            print(msg)
            process(TARGET, msg)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def send():
    global TARGET
    global RESPONSE
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET, PORT))
        sock.sendto(str(RESPONSE).encode(), (TARGET, PORT))
        print("Result: " + str(RESPONSE))
        sock.close()
    except Exception as e:
        print("Send Error: " + str(e))

def process(addr, msg):
    global RESPONSE
    print(addr + ":" + str(msg))
    # Load JSON here instead of splitting the text.
    j = json.loads(msg)

    try:
        if (j["type"] == "register"):
            username = j["from"]["username"]
            password = j["from"]["password"]
            db.register(username,password)
        elif (j["type"] == "check_available"):
            username = j["from"]["username"]
            RESPONSE = str(db.check_available(username))
            sthread = Thread(target=send)
            sthread.start()
            sthread.join()
        elif (j["type"] == "login"):
            username = j["from"]["username"]
            password = j["from"]["password"]
            ip = addr
            RESPONSE = db.login(username,password,ip)
            sthread = Thread(target = send)
            sthread.start()
            sthread.join()
        elif(j["type"] == "logout"):
            db.logout(j["from"]["id"])
        elif (j["type"] == "get_online"):
            id = j["from"]["id"]
            RESPONSE = db.get_online_list()
            result = []
            for i in RESPONSE:
                if (i.id != id):
                    line = {
                        "userID": i.id, 
                        "username": i.username,
                        "ip": i.ip
                        }
                    result.append(line)

        
            RESPONSE = {"online_users": []}
            RESPONSE["online_users"] = result
            RESPONSE = json.dumps(RESPONSE)
            sthread = Thread(target=send)
            sthread.start()
            sthread.join()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)

    return 0
    
if __name__ == '__main__':
    lthread = Thread(target=listen)
    lthread.start()  # threadleri başlatıyoruz.
    lthread.join()  # threadleri ana thread'e (main fonksiyonuna bağlıyoruz)