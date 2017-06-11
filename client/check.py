#!/usr/bin/python3

import shutil
import sys
import hashlib
import gnupg
from socket import *
from os.path import exists as path_exists
from os import remove
from filecmp import cmp as diff
from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, call, DEVNULL
from time import time

OUTPUT_FILE = '.OUTPUT_TEMP'
TIMEOUT = 2

gpg = gnupg.GPG(gnupghome="./.gpghome")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def clean_up(filename):
    if path_exists(OUTPUT_FILE):
        remove(OUTPUT_FILE)
    if path_exists(filename):
        remove(filename)

def check_program(filename):
    failed = call(["gcc",filename, "-o", filename[:-2]], stdout=DEVNULL, stderr=DEVNULL, timeout=TIMEOUT)
    if failed: 
        print("Compilation Error")

def decode(f):
    dec = open('.' + f[:-4]+".dec","w")
    with open(f) as fi:
        decrypted_data = gpg.decrypt(fi.read(), passphrase="unlock")
        dec.write(str(decrypted_data))

def run_program(exe, TEST_CASES):
    i = 0
    const = len(TEST_CASES)
    decode('hashes.enc')
    hashes = open('.hashes.dec').readlines()
    if md5('mykeyfile.asc') != hashes[0][:-1]:
        print("key doesnt match")
        return -2
    correct = 1
    for test_case in TEST_CASES:
        decode(test_case)
        decoded_file = '.' + test_case[:-3] + 'dec'
        if md5(decoded_file) != hashes[1+i][:-1]:
            print(md5(decoded_file) + '!=' + hashes[1+i][:-1])
            return -1
        ipf = open(decoded_file)
        opf = open(OUTPUT_FILE, 'w')
        TLE = False
        failed = False
        start_time = time()
        try:
            run(exe, stdin=ipf, stdout=opf, stderr=PIPE, timeout=TIMEOUT,
                check=True)
        except TimeoutExpired:
            TLE = True
            pass
        except CalledProcessError as e:
            failed = True
        finally:
            ipf.close()
            opf.close()
        end_time = time()
        i += 1

        status = "failed" if (not md5(OUTPUT_FILE) == hashes[i+const][:-1] or failed) else "passed"
        if status == "failed":
            correct = 0

        print(i, (end_time - start_time) if not TLE else "\tTLE\t", status, sep='\t')
        clean_up(decoded_file)
    
    clean_up(".hashes.dec")
    clean_up(exe)


    #try:
    if(correct == 1):
        s = socket()
        s.connect(("localhost",9999))
        ok = s.recv(1024)

        if ok.decode("utf-8") == "ok":
            flag = True
        else:
            flag = False
            print("Cant connect")

        while flag:
            usr = input("Username: ")
            s.send(str.encode(usr))
            psw = input("Password: ")
            s.send(str.encode(psw))
            if s.recv(1024).decode("utf-8") == "True":
                print("Submission sent!")
                flag = False
            else:
                print("Incorrect login details, try again")

        f = open(exe+'.c').read()
        key_data = open('./mykeyfile.asc').read()
        server_key = gpg.import_keys(key_data)
        public_keys = gpg.list_keys()
        encrypted_data = gpg.encrypt(f, public_keys.uids[0][19:-1], always_trust=True)
        s.send(str.encode(str(encrypted_data)))
        s.close()

    
    shutil.rmtree('./.gpghome')
    #except:
     #   print("Error!")


def main():
    if (len(sys.argv) < 3):
        return
    filename = sys.argv[1]
    datafiles = sys.argv[2:]
    iofiles = []
    for f in datafiles:
        if (not path_exists(f)):
            print(f, "does not exist")
            return
    
    check_program(filename)

    if path_exists(filename[:-2]):
        print("# Test case\tTime taken\tPassed")
        print("#--------------------------------------")
        run_program(filename[:-2], datafiles)

if __name__ == "__main__":
    main()
