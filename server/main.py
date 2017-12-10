from tools import GenerateKey, ExportKey, EncodeFiles, CleanUp
from head import Head
from server import Server
from os.path import exists as path_exists
from os import makedirs
from random import sample
import json

print("\nOffline Judge (Server)")
print("1. Start a new Test")
print("2. Run the Server")
print("3. Cleanup Server")

opt = input("Enter selection: ")

alpha = "qwertyuiopasdfghjklzxcvbnm1234567890";
usr = "iiita"
psw = "".join(sample(alpha, 15))
home = './gpghome/'
src = './tests/'
dest = './testfiles/'
sym_passkey = "".join(sample(alpha, 10))

if opt == str(1):
    # Generate GNUPG Key
    gen = GenerateKey(home)
    print("\nServer")
    print("Encrypting test cases...")
    key = gen.generate(usr, psw)
    
    # Export generated key
    exp = ExportKey(home)
    public_key = exp.export(key)
    if not path_exists(dest):
        makedirs(dest)  
    with open('./testfiles/public_key.asc', 'w') as f:
        f.write(public_key)

    # Write details of test into a head file
    h = Head(src) 
    inputs = h.get_inputs()
    input_hashes = h.gen_in_hashes()
    output_hashes = h.gen_out_hashes()
    scores = h.get_scores('./tests/scores')
    key_hash = h.md5("./testfiles/public_key.asc")
    port = int(input("Enter port number: "))
    server = h.getIP(port)
    print("Server details- " + server['ip'] + ":" + str(server['port']))
    h.write_json('./tests/head.txt', inputs, input_hashes, output_hashes, scores, key_hash, server)

    # Encrypt all input files
    enc = EncodeFiles(home)
    enc.encode(src, dest, sym_passkey)
    l = enc.get_files(src, 'txt')
    print("Encoded " + str(len(l)) + " files")
    print("\nPasskey: " + sym_passkey + "\n")

    # Store server details
    json_data = {
        "gpg-username": usr,
        "gpg-password": psw,
        "passkey": sym_passkey,
        "ip": server['ip'],
        "port": server['port'],
    }

    with open(".server", 'w') as fp:
            json.dump(json_data, fp, indent=4)

elif opt == str(2):
    json_data = json.load(open(".server", "r"))
    passkey = json_data["passkey"]
    port = int(json_data["port"])
    server = Server(home, "", port, passkey, 2)
    server.runServer("./Files/", "./results.json")

elif opt == str(3):
    CleanUp()


