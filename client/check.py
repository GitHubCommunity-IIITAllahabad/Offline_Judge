#!/usr/bin/python3

import shutil
import sys
import hashlib
import gnupg
import json
from socket import *
from os.path import exists as path_exists
from os import remove
from filecmp import cmp as diff
from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, call, DEVNULL
from time import time

OUTPUT_FILE = 'testfiles/.OUTPUT_TEMP'
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
    dec = open("testfiles/" + '.' + f[:-4]+".dec","w")
    with open("testfiles/" + f) as fi:
        decrypted_data = gpg.decrypt(fi.read(), passphrase="unlock")
        dec.write(str(decrypted_data))

def run_program(exe, TEST_CASES, inHashes, outHashes):
    i = 0
    const = len(TEST_CASES)
    correct = True
    for test_case in TEST_CASES:
        decode(test_case)
        decoded_file = 'testfiles/' + '.' + test_case[:-3] + 'dec'
        if md5(decoded_file) != inHashes[test_case[:-4]+'.txt']:
            print(md5(decoded_file) + '!=' + inHashes[test_case[:-4]+'.txt'])
            return -1
        ipf = open(decoded_file)
        opf = open(OUTPUT_FILE, 'w')
        TLE = False
        failed = False
        start_time = time()
        try:
            run("./"+exe, stdin=ipf, stdout=opf, stderr=PIPE, timeout=TIMEOUT,
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

        status = "failed" if (md5(OUTPUT_FILE) != outHashes[test_case[:-4]+'.out'] or failed) else "passed"
        if status == "failed":
            correct = False
            print(md5(OUTPUT_FILE) +'!='+ outHashes[test_case[:-4]+'.out'])
        i += 1
        print(i, (end_time - start_time) if not TLE else "\tTLE\t", status, sep='\t')
        clean_up(decoded_file)
    
    clean_up(exe)
    return correct



def post_scores(submissions):
    #try:
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
            flag = False
        else:
            print("Incorrect login details, try again")
    s.send(str.encode(str(len(submissions))))
    s.recv(1024)
    for file in submissions:
        s.send(str.encode(file))
        s.recv(1024)
        f = open(file).read()
        key_data = open('./testfiles/public_key.asc').read()
        server_key = gpg.import_keys(key_data)
        public_keys = gpg.list_keys()
        encrypted_data = gpg.encrypt(f, public_keys.uids[0][19:-1], always_trust=True)
        s.send(str.encode(str(encrypted_data)))

    if s.recv(1024).decode("utf-8") == "received":
        print("Successfully submitted!")
    else:
        print("There was an error in submitting your answers")
    s.close()


    
    shutil.rmtree('./.gpghome')
    #except:
     #   print("Error!")


def main():

    decode("head.enc")
    json_data = json.load(open("./testfiles/.head.dec", "r"))
    clean_up("./testfiles/.head.dec")

    inputs = json_data['inputs']
    input_hashes = json_data['input_hashes']
    output_hashes = json_data['output_hashes']
    key_hash = json_data['key_hash']

    if key_hash != md5("./testfiles/public_key.asc"):
        print("Error: The public key has been modified!")
        return -1

    values = list(inputs.values())
    datafiles = []
    for x in values:
        datafiles = datafiles + list(x)
    for f in datafiles:
        if (not path_exists("testfiles/" + f)):
            print(f, "does not exist")
            return
    correct = []
    for question in inputs:
        filename = input("Enter filename for question " + str(question) + ": ")
        if filename == "":
            continue
        check_program(filename)

        if path_exists(filename[:-2]):
            print("# Test case\tTime taken\tPassed")
            print("#--------------------------------------")
            if(run_program(filename[:-2], inputs[question], input_hashes, output_hashes) == True):
                correct += [filename]
    print(correct)
    post_scores(correct)


if __name__ == "__main__":
    main()
