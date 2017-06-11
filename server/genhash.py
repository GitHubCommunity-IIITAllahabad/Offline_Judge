import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
	f = open("tests/hashes.txt", "w")
	while True:
		fname = input("File to be hashed: ")
		if fname == "0":
			break
		h = md5("tests/"+fname)
		f.write(h + "\n")
		print("Hashed " + fname + ": " + h)

	f.close()

if __name__ == "__main__":
	main()
	
