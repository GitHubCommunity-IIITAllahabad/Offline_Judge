import gnupg
import os
from socket import *
from threading import Thread

def clientHandler():
    while True:
        #try:
        print("Waiting")
        conn, addr = s.accept()
        print (addr, "is connected")
        conn.send(str.encode("ok"))
        flag = True
        while flag:
            usr = conn.recv(1024)
            psw = conn.recv(1024)
            if usr == psw:                          #LDAP Script goes here
                conn.send(str.encode("True"))
                flag = False
            else:
                print("Failed authentication of " + usr.decode("utf-8"))
                conn.send(str.encode("False"))
        num = int(conn.recv(1024).decode("utf-8"))
        conn.send(str.encode("ok"))
        print(num)
        while num > 0:
            num -= 1
            name = str(conn.recv(1024).decode("utf-8"))
            conn.send(str.encode("ok"))
            data = conn.recv(1024)  
            decrypted_data = gpg.decrypt(str(data.decode("utf-8")), passphrase=passkey)
            decrypted_string = str(decrypted_data)
            open("Files/"+usr.decode("utf-8")+"_"+name, "w").write(decrypted_string)
            print("Successfully received " + name +" from " + usr.decode("utf-8"))

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
