import hashlib
import os
import json

class Head:
    
    def __init__(self, src):
        self.src = src 

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_files(self, ext):
        all_files = os.listdir(self.src)
        submissions = [fname for fname in all_files if fname.endswith(ext)]
        return submissions

    def get_inputs(self):
        all_files = os.listdir(self.src)
        inputs = {}
        i = 1
        while True:
            fs = [fname[:-4] + '.enc' for fname in all_files if (fname.startswith(str(i) + "_") and fname.endswith("txt"))]
            if fs == []:
                break
            inputs[str(i)] = fs
            i += 1
        return inputs

    def gen_in_hashes(self):
        allfiles = self.get_files(".txt")
        hashes = {}
        for file in allfiles:
            hashes[file] = self.md5(self.src+file)
        return hashes

    def gen_out_hashes(self):
        allfiles = self.get_files(".out")
        hashes = {}
        for file in allfiles:
            hashes[file] = self.md5(self.src+file)
        return hashes

    def get_scores(self, file):
        f = open(file,"r")
        i = 1
        scores = {}
        for line in f.readlines():
            scores[str(i)] = int(line)
            i += 1
        return scores

    def write_json(self, dest, inputs, input_hashes, output_hashes, scores, key_hash):
        json_data = {
            'inputs' : inputs,
            'input_hashes' : input_hashes,
            'output_hashes' : output_hashes,
            'scores': scores,
            'key_hash' : key_hash
        }

        with open(dest, 'w') as fp:
            json.dump(json_data, fp, indent=4)

