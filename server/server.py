import gnupg
import os
from socket import *
from threading import Thread, Lock
import json

class Server:

    def __init__(self, home, HOST, PORT, passkey, MAX_CONNS):

        self.gpg = gnupg.GPG(homedir=home)
        self.passkey = passkey
        self.lock = Lock()
        self.HOST = HOST
        self.PORT = PORT
        self.MAX_CONNS = MAX_CONNS   #maximum simultaneous connections

    def runServer(self, dest, results_path):

        self.dest = dest
        self.results_path = results_path

        self.s = socket()
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(5)

        if not os.path.exists(dest):
            os.makedirs(dest)
        print ("Server is running")

        for i in range(self.MAX_CONNS):
            Thread(target=self.clientHandler).start()

    def clientHandler(self):
        while True:
            try:
                print("Waiting")
                conn, addr = self.s.accept()
                print (addr, "is connected")
                conn.send(str.encode("ok"))
                flag = True
                while flag:
                    usr = conn.recv(1024).decode("utf-8")
                    psw = conn.recv(1024).decode("utf-8")
                    if usr == psw:                          #LDAP Script goes here
                        conn.send(str.encode("True"))
                        flag = False
                    else:
                        print("Failed authentication of " + usr)
                        conn.send(str.encode("False"))
                final_score = int(conn.recv(1024).decode("utf-8"))
                conn.send(str.encode("ok"))
                self.json_write(usr, final_score)
                num = int(conn.recv(1024).decode("utf-8"))
                conn.send(str.encode("ok"))
                print(usr + " score: " + str(final_score))
                while num > 0:
                    num -= 1
                    name = str(conn.recv(1024).decode("utf-8"))
                    print("Receiving " + name +" from " + usr)
                    conn.send(str.encode("ok"))
                    data = conn.recv(5120)
                    #print("Enc:"+data.decode("utf-8")+";") 
                    decrypted_data = self.gpg.decrypt(str(data.decode("utf-8")), passphrase=self.passkey)
                    decrypted_string = str(decrypted_data)
                    open(self.dest+usr+"_"+name, "w").write(decrypted_string)
                    print("Received " + name)
                    conn.send(str.encode("received"))
                print("\n")
            except:
               print("There was some error %s" % (addr, ))               #mostly due to Ctrl+C on client's side

    def json_write(self, name, score):
        self.lock.acquire()
        result = {}
        if os.path.isfile(self.results_path): 
            f = open(self.results_path, "r")
            result = json.load(f)
        f = open(self.results_path, "w")
        result[name] = score
        json.dump(result, f, sort_keys=True, indent=4)
        f.close()
        self.lock.release()


