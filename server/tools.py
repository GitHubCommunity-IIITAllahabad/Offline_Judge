import os

class GenerateKey:
    """Generates a new RSA key with given username and password"""
    def __init__(self, home):
        import gnupg
        self.gpg = gnupg.GPG(homedir=home)
        
    def generate(self, usr, psw):

        input_data = self.gpg.gen_key_input(
            name_email=usr,
            passphrase=psw,
            key_type='RSA')
        
        key = self.gpg.gen_key(input_data)
        return key

class ExportKey:
    """Exports the public key of given fingerprint"""
    def __init__(self, home):
        import gnupg
        self.gpg = gnupg.GPG(homedir=home)

    def export(self, key):
        ascii_armored_public_keys = self.gpg.export_keys(key)
        return ascii_armored_public_keys

class EncodeFiles:
    """Encrypts the files in src and puts them in dest with given passkey"""
    def __init__(self, home):
        import gnupg
        self.gpg = gnupg.GPG(homedir=home)

    def get_files(self, src, ext):
        all_files = os.listdir(src)
        inputs = [fname for fname in all_files if fname.endswith(ext)]
        return inputs

    def encode(self, src, dest, passkey):
        inputs = self.get_files(src, ".txt")
        if not os.path.exists(dest):
            os.makedirs(dest)
        for f in inputs:
            enc = open(dest+f[:-4]+".enc","w")
            with open(src+f) as fi:
                encrypted_data = self.gpg.encrypt(fi.read(), encrypt=False, symmetric="AES256", passphrase=passkey)
                enc.write(str(encrypted_data))            

class CleanUp:
    """Delete all server files/folders"""
    def __init__(self):
        import shutil
        dirs = [
            './Files', 
            './gpghome', 
            './__pycache__',
            './testfiles'
        ]

        files = [
            './tests/head.txt',
            './results.json'
        ]

        for folder in dirs:
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(e)

        for file in files:
            try:
                os.remove(file)
            except Exception as e:
                print(e)



