from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import sys, getopt, os, struct

#encrypt.py <inputfile> <outputfile> <password> <keyfile>
def main(argv):
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    password = sys.argv[3]
    keyfile = sys.argv[4]
    print(inputfile)
    print(outputfile)
    print(password)
    print(keyfile)

    iterations = 5000
    key = ''
    salt = os.urandom(32)

    key = PBKDF2(password, salt, dkLen=32, count=iterations)
    iv = os.urandom(AES.block_size)

    encobj = AES.new(key, AES.MODE_CBC, iv)

    with open(inputfile, 'rb') as ifile:
        plaintext = ifile.read()

    plaintext = plaintext + b"\0" * (AES.block_size - len(plaintext) % AES.block_size)
    encoded = iv + encobj.encrypt(plaintext)
    with open(outputfile, 'wb') as ofile:
        ofile.write(encoded)

    with open(keyfile, 'wb') as kfile:
        kfile.write(key)

if __name__ == "__main__":
    main(sys.argv[1:])





#    filesize = os.path.getsize(inputfile)
#
 #   with open(inputfile, 'rb') as infile:
  #      with open(outputfile, 'wb') as outfile:
   #         outfile.write(struct.pack('<Q', filesize))
    ###      while True:
       #         chunk = infile.read(64*1024)
        #        if len(chunk) == 0:
         #           break
          #      elif len(chunk) % 16 != 0:
           #         chunk += ' ' * (16 - len(chunk) % 16)
#
 #               outfile.write(encobj.encrypt(chunk))







#key = 'mysecretpassword'
#iv = os.urandom(16)

#plaintext = "wow this is good"

#encobj = AES.new(key, AES.MODE_CBC, iv)

#ciphertext = encobj.encrypt(plaintext)

#print(" ".join(hex(n) for n in ciphertext))

#decobj = AES.new(key, AES.MODE_CBC, iv)
#plaintext = decobj.decrypt(ciphertext)

#print(plaintext)