# Offline_Judge

Requirements: Python3 with GnuPG module

Steps:
1) Navigate to the server directory and run main.py
2) Create a new server key-pair and the copy the key displayed
3) Export the public-key by pasting the copied key (A file will be created in dirs './Encrypted' and './tests')
4) Generate hashes of the following files in the exact same order:
	* mykeyfile.asc
	* in1.txt
	* in2.txt
	* out1
	* out2
5) Encode all the input files and hashes.txt
6) Copy all the contents of the directory "Encrypted" to the client folder (These are what will be handed over to the student)
7) Run the check.py script by typing the following command:
	$ python3 check.py ./a.c in1.enc in2.enc
8) If the code is correct the script prompts for your LDAP credentials and posts the results to the server
