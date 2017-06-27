# Offline_Judge

Requirements: Python3 with GnuPG module

Instructions:-

Server-side:
1) Navigate to the server directory and run main.py
2) Create a new server key-pair and then copy the key displayed
3) Export the public-key by pasting the copied key (A file will be created in the directory './testfiles/')
4) Generate head.txt which contains details of each question and their hashes
5) Encode all the input files and head.txt
6) Copy the "testfiles" folder over to the client directory (These are what will be handed over to the student)
7) Run the server and enter the passphrase set in step 2
8) Submissions will be saved in the directory named "Files"

Client-side:
1) Run the check.py script
2) Enter the filename (ex. "1.c") for each question (leave it blank if you don't want to attempt)
3) Finally the script prompts for your LDAP credentials in order to post the results to the server
