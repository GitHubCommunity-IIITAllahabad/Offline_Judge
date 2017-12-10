#!/usr/bin/python3

import shutil
import sys
import hashlib
import gnupg
import json
from getpass import getpass
from socket import *
from os.path import exists as path_exists
from os import remove
from filecmp import cmp as diff
from subprocess import run, PIPE, CalledProcessError, TimeoutExpired, call, DEVNULL
from time import time

def main():

    home = "./.gpghome/"
    passkey = input("Enter passkey: ")
    src = "./testfiles/"
    keyFile = src + "public_key.asc"
    timeout = 2

    tools = Tools(src, home, passkey)
    inputs, input_hashes, output_hashes, scores, key_hash, server = tools.extractHead("head.enc")

    if tools.checkKeyFile(key_hash) == 0: return -1
    if tools.checkIfExists(inputs) == 0: return 404


    judge = Judge(tools, src, inputs, input_hashes, output_hashes, timeout)
    accepted = judge.evaluateAll()
    finalScore = judge.calcScore(scores, accepted)

    net = Client(server, home, keyFile)
    net.post_scores(accepted, finalScore)
    shutil.rmtree(home)

class Tools:

    def __init__(self, src, home, passkey):
        self.src = src
        self.passkey = passkey
        self.home = home
        pass

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def clean_up(self, filename):
        if path_exists(filename):
            remove(filename)

    def decode(self, f):
        gpg = gnupg.GPG(homedir=self.home)
        dec_name = self.src + '.' + f[:-4]+".dec"
        dec = open(dec_name,"w")
        with open(self.src + f) as fi:
            decrypted_data = gpg.decrypt(fi.read(), passphrase=self.passkey)
            dec.write(str(decrypted_data))
        return dec_name

    def extractHead(self, f):
        headDec = self.decode(f)
        json_data = json.load(open(headDec, "r"))
        self.clean_up(headDec)

        inputs = json_data['inputs']
        input_hashes = json_data['input_hashes']
        output_hashes = json_data['output_hashes']
        scores = json_data['scores']
        key_hash = json_data['key_hash']
        server = json_data['server']

        return inputs, input_hashes, output_hashes, scores, key_hash, server

    def checkIfExists(self, files):
        datafiles = []
        for question in list(files.values()):
            for testfile in question:
                datafiles += [testfile]

        for f in datafiles:
            if (not path_exists(self.src + f)):
                print(f, "does not exist")
                return 0

        return 1

    def checkKeyFile(self, key_hash):
        if key_hash != self.md5(self.src + "public_key.asc"):
            print("Error: The public key has been modified!")
            return 0
        return 1

class Judge:

    def __init__(self, tools, src, inputs, input_hashes, output_hashes, TIMEOUT):
        self.tools = tools
        self.src= src
        self.inputs = inputs
        self.input_hashes = input_hashes
        self.output_hashes = output_hashes
        self.TIMEOUT = TIMEOUT

    def compile(self, filename):
        failed = call(["gcc",filename, "-o", self.src + filename[:-2]], stdout=DEVNULL, stderr=DEVNULL, timeout=self.TIMEOUT)
        if failed: 
            print("Compilation Error")
        return self.src + filename[:-2]

    def evaluateAll(self):
        accepted = []
        for question in range(1, len(self.inputs) + 1):
            filename = input("Enter filename for question " + str(question) + ": ")
            if filename == "":
                continue
            exe = self.compile(filename)
            
            if path_exists(exe):
                print("# Test case\tTime taken\Status")
                print("#--------------------------------------")
                if(self.evalQuestion(exe, question) == True):
                    accepted += [filename]

        return accepted

    def evalQuestion(self, exe, question):
        TEST_CASES = self.inputs[str(question)]
        correct = True

        for test_case in TEST_CASES:
            if(self.evalTestCase(exe, test_case) == False):
                correct = False        
        
        self.tools.clean_up(exe)
        return correct

    def evalTestCase(self, exe, test_case):
        OUTPUT_FILE = self.src + '.OUTPUT_TEMP'
        self.tools.decode(test_case)
        decoded_file = self.src + '.' + test_case[:-3] + 'dec'

        if self.tools.md5(decoded_file) != self.input_hashes[test_case[:-4]+'.txt']:
            print("Incorrect checksum!")
            return False

        ipf = open(decoded_file)
        opf = open(OUTPUT_FILE, 'w')
        TLE = False
        failed = False

        start_time = time()
        try:
            run(exe, stdin=ipf, stdout=opf, stderr=PIPE, timeout=self.TIMEOUT,
                check=True)
        except TimeoutExpired:
            TLE = True
            pass
        except CalledProcessError as e:
            failed = True
        finally:
            end_time = time()
            ipf.close()
            opf.close()
            outmd5 = self.tools.md5(OUTPUT_FILE)
            self.tools.clean_up(decoded_file)
            self.tools.clean_up(OUTPUT_FILE)

        status = "failed" if (outmd5 != self.output_hashes[test_case[:-4]+'.out'] or failed or TLE) else "passed"

        if status == "failed":
            correct = False
        else:
            correct = True

        print((end_time - start_time) if not TLE else "\tTLE\t", status, sep='\t')

        return correct

    def calcScore(self, scores, accepted):
        finalScore = 0
        
        for question in accepted:
            finalScore += scores[question[:-2]]

        return finalScore

class Client:
    def __init__(self, server, home, keyFile):
        self.ip = server['ip']
        self.port = server['port']
        self.home = home
        self.keyFile = keyFile
        self.gpg = gnupg.GPG(homedir=self.home)

    def connect(self):
        flag = False
        try:
            print("Waiting for connection...")
            s = socket()
            while True:
                try:
                    s.connect((self.ip, self.port))
                    break
                except:
                    pass
            ok = s.recv(1024)

            if ok.decode("utf-8") == "ok":
                print("Connected!")
                flag = True
        except:
                print("Unable to connect")
        return s, flag

    def authenticate(self, s):
        flag = True
        while flag:
            usr = input("\nUsername: ")
            s.send(str.encode(usr))
            psw = getpass("Password: ")
            s.send(str.encode(psw))
            if s.recv(1024).decode("utf-8") == "True":
                flag = False
            else:
                print("Incorrect login details, try again")

    def getFingerprint(self):
        key_data = open(self.keyFile).read()
        server_key = self.gpg.import_keys(key_data)
        public_keys = self.gpg.list_keys()
        return public_keys[0]['fingerprint']

    def post_scores(self, submissions, final_score):
        try:
            s, flag = self.connect()
            if flag == False: return 0
            self.authenticate(s)
            fingerprint = self.getFingerprint()
            success = 0
            s.send(str.encode(str(final_score)))
            s.recv(1024)
            s.send(str.encode(str(len(submissions))))
            s.recv(1024)
            for file in submissions:
                s.send(str.encode(file))
                s.recv(1024)
                f = open(file).read()
                encrypted_data = self.gpg.encrypt(f, fingerprint, always_trust=True)
                s.send(str.encode(str(encrypted_data)))
                if s.recv(1024).decode("utf-8") == "received":
                    success += 1
                else:
                    print("Failed to send " + file)

            if success == len(submissions):
                print("Successfully submitted!")
            else:
                print("There was an error in submitting your answers")
            s.close()
        except:
            print("Error!")


if __name__ == "__main__":
    main()
    
