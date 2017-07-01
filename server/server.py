import gnupg
import os
from socket import *
from threading import Thread, Lock
import json

lock = Lock()

def json_write(name, score):
    lock.acquire()
    result = {}
    if os.path.isfile("./results.json"): 
        f = open("./results.json", "r")
        result = json.load(f)
    f = open("./results.json", "w")
    result[name] = score
    json.dump(result, f, sort_keys=True, indent=4)
    f.close()
    lock.release()

def clientHandler():
    while True:
        #try:
        print("Waiting")
        conn, addr = s.accept()
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
        json_write(usr, final_score)
        conn.send(str.encode("ok"))
        num = int(conn.recv(1024).decode("utf-8"))
        conn.send(str.encode("ok"))
        print(usr + ": " + str(final_score))
        while num > 0:
            num -= 1
            name = str(conn.recv(1024).decode("utf-8"))
            conn.send(str.encode("ok"))
            data = conn.recv(1024)  
            decrypted_data = gpg.decrypt(str(data.decode("utf-8")), passphrase=passkey)
            decrypted_string = str(decrypted_data)
            open("Files/"+usr+"_"+name, "w").write(decrypted_string)
            print("Successfully received " + name +" from " + usr)

        conn.send(str.encode("received"))
        print("\n")
        #except:
        #   print("There was some error")               #mostly due to Ctrl+C on client's side

def main():

    global gpg
    global passkey
    global HOST, PORT, s

    gpg = gnupg.GPG(gnupghome='./gpghome')
    passkey=input("Enter server's passphrase: ")
    if passkey == "":
        passkey = "iiita321"

    HOST = "" #localhost
    PORT = 9999
    MAX_CONNS = 2   #maximum simultaneous connections

    s = socket()
    s.bind((HOST, PORT))
    s.listen(5)

    if not os.path.exists("./Files"):
        os.makedirs("./Files")

        print ("Server is running")

    for i in range(MAX_CONNS):
        Thread(target=clientHandler).start()

    #s.close()

if __name__ == "__main__":
    main()
