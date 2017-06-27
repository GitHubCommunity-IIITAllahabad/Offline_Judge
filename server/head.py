import hashlib
import os
import json

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_files(ext):
    all_files = os.listdir("./tests/")
    submissions = [fname for fname in all_files if fname.endswith(ext)]
    return submissions

def get_inputs():
    all_files = os.listdir("./tests/")
    inputs = {}
    i = 1
    while True:
        fs = [fname[:-4] + '.enc' for fname in all_files if (fname.startswith(str(i) + "_") and fname.endswith("txt"))]
        if fs == []:
            break
        inputs[str(i)] = fs
        i += 1
    return inputs

def gen_in_hashes():
    allfiles = get_files(".txt")
    hashes = {}
    for file in allfiles:
        hashes[file] = md5("./tests/"+file)
    return hashes

def gen_out_hashes():
    allfiles = get_files(".out")
    hashes = {}
    for file in allfiles:
        hashes[file] = md5("./tests/"+file)
    return hashes

def write_json(inputs, input_hashes, output_hashes, key_hash):
    json_data = {
        'inputs' : inputs,
        'input_hashes' : input_hashes,
        'output_hashes' : output_hashes,
        'key_hash' : key_hash
    }

    with open('./tests/head.txt', 'w') as fp:
        json.dump(json_data, fp, indent=4)

def main():
    inputs = get_inputs()
    input_hashes = gen_in_hashes()
    output_hashes = gen_out_hashes()
    key_hash = md5("./testfiles/public_key.asc")
    write_json(inputs, input_hashes, output_hashes, key_hash)  
    print("Successfully written input filenames and hashes to JSON file")  

if __name__ == "__main__":
    main()

