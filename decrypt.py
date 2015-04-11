from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import sys, getopt, os, struct

#decrypt.py <encoded file> <keyfile> <decoded file name>
def main(argv):
    encfile = sys.argv[1]
    keyfile = sys.argv[2]
    decfile = sys.argv[3]

    with open(keyfile, 'rb') as kfile:
        key = kfile.read()

    with open(encfile, 'rb') as efile:
        ciphertext = efile.read()

    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    dec = plaintext.rstrip(b"\0")

    with open(decfile[:-4], 'wb') as dfile:
        dfile.write(dec)

if __name__ == "__main__":
    main(sys.argv[1:])