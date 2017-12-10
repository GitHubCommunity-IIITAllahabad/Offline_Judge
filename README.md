# Offline_Judge

Requirements: Python3 with GnuPG module

Instructions:-

Server-side:
1) Navigate to the server directory and copy the following files into the tests directory: <br />
	a) Input files (Format: QuestionNum_TestCaseNum.txt) <br /> 
	b) Output files (Format: QuestionNum_TestCaseNum.out) <br />
	c) "scores" file containing the weightage of each question <br />
2) Run the main.py script
3) Select "Start a new Test"
4) Enter port number on which the server should run for accepting scores
5) Copy the "testfiles" folder over to the client directory (These are what will be handed over to the student)
6) Run the Server
7) Submissions will be saved in the directory named "Files" and the scores will be saved in results.json

Client-side:
1) Run the check.py script
2) Enter the required passkey
3) Enter the filename (ex. "1.c") for each question (leave it blank if you don't want to attempt)
4) Finally the script prompts for your credentials in order to post the results to the server

