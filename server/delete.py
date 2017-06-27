import shutil
import os

def main():

    shutil.rmtree("./Files")
    shutil.rmtree("./gpghome")
    shutil.rmtree("./__pycache__")
    shutil.rmtree("./testfiles")
    os.remove("./tests/head.txt")

    print("Cleaned up server files/folders\n")

if __name__ == "__main__":
    main()