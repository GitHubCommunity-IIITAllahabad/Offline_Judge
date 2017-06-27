#!/usr/bin/python3

import os
import gnupg

def get_files(ext):
    """Gives list of all submission available"""
    all_files = os.listdir(os.getcwd()+"/tests/")
    inputs = [fname for fname in all_files
                   if fname.endswith(ext)]
    print(inputs)
    return inputs

def encode():
    inputs = get_files(".txt")
    if not os.path.exists("./testfiles"):
        os.makedirs("./testfiles")
    for f in inputs:
        enc = open("testfiles/"+f[:-4]+".enc","w")
        with open("./tests/"+f) as fi:
            encrypted_data = gpg.encrypt(fi.read(), recipients=None, symmetric="AES256", passphrase=passkey)
            enc.write(str(encrypted_data))


def decode():
    inputs = get_files(".enc")
    for f in inputs:
        dec = open(f[:-4]+".dec","w")
        with open('./testfiles/'+f) as fi:
            print(fi.read())
            decrypted_data = gpg.decrypt(fi.read(), passphrase=passkey)
            dec.write(str(decrypted_data))

def main():
    global gpg, passkey
    gpg = gnupg.GPG(gnupghome='./gpghome')
    passkey="unlock"
    encode()
    #decode()

if __name__ == "__main__":
	main()
