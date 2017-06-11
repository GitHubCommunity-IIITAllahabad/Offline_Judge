import gnupg
import os

def main():
	key = input("Enter key: ")
	gpg = gnupg.GPG(gnupghome='./gpghome')
	ascii_armored_public_keys = gpg.export_keys(key)
	ascii_armored_private_keys = gpg.export_keys(key, True)
	if not os.path.exists("./Encrypted"):
	        os.makedirs("./Encrypted")	
	with open('Encrypted/mykeyfile.asc', 'w') as f:
	    f.write(ascii_armored_public_keys)
	with open('tests/mykeyfile.asc', 'w') as f:
	    f.write(ascii_armored_public_keys)

if __name__ == "__main__":
	main()
