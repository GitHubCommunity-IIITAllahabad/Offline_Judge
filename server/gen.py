import os
import gnupg

def main():
	#os.system('rm -rf ./gpghome')
	gpg = gnupg.GPG(gnupghome='./gpghome')
	
	usr = input("Enter a new username: ")
	if usr == "":
		usr = "admin@iiita.ac.in"

	psw = input("Enter a new password: ")
	if psw == "":
		psw = "iiita321"

	input_data = gpg.gen_key_input(
	    name_email=usr,
	    passphrase=psw)
	key = gpg.gen_key(input_data)
	print("Your key: " + str(key))

if __name__ == "__main__":
	main()
