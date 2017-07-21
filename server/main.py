from tools import GenerateKey, ExportKey, EncodeFiles, CleanUp
from head import Head
from server import Server
from os.path import exists as path_exists
from os import makedirs

print("\nOffline Judge (Server)")
print("1. Generate Server's key-pair")
print("2. Export Server's public-key")
print("3. Generate head.txt")
print('4. Encode test files')
print("5. Run the server")
print("6. Cleanup server")
print("7. Exit")

opt = input("Enter selection: ")

home = './gpghome/'
src = './tests/'
dest = './testfiles/'
sym_passkey = 'unlock'

if opt == str(1):
    gen = GenerateKey(home)
    print("\nServer")
    usr = input("Enter a new username: ")
    psw = input("Enter a new password: ")
    key = gen.generate(usr, psw)
    print("Your key: " + str(key))

elif opt == str(2):
    exp = ExportKey(home)
    key = input("Enter key to export: ")
    public_key = exp.export(key)
    if not path_exists(dest):
        makedirs(dest)  
    with open('./testfiles/public_key.asc', 'w') as f:
        f.write(public_key)
    print("Public key exported: './testfiles/public_key.asc'")

elif opt == str(3):
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
    print("Successfully generated JSON file")  

elif opt == str(4):
    enc = EncodeFiles(home)
    enc.encode(src, dest, sym_passkey)
    l = enc.get_files(src, 'txt')
    print("Encoded " + str(len(l)) + " files: " + str(l))

elif opt == str(5):
    passkey = input("Enter server's passphrase: ")
    port = int(input("Enter port number: "))
    server = Server(home, "", port, passkey, 2)
    server.runServer("./Files/", "./results.json")

elif opt == str(6):
    CleanUp()
