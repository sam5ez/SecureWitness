import sys
import hashlib
from tkinter import *
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import sys, getopt, os, struct

def encrypt():
    inputfile = ginputfile.get()
    outputfile = goutputfile.get()
    password = gpassword.get()
    keyfile = gkeyfile.get()

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

def decrypt():
    encfile = gencfile.get()
    keyfile = gkeyfile2.get()
    decfile = gdecfile.get()

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

def producemd5():
    sourcefile = gsourcefile.get()

    with open(sourcefile, 'rb') as sfile:
        source = sfile.read()

    output = hashlib.md5(source).digest()

    with open("md5", 'wb') as ofile:
        ofile.write(output)

def checkmd5():
    downloadedfile = gdownloadedfile.get()
    md5file = gmd5hashfile.get()

    with open(downloadedfile, 'rb') as dfile:
        downloaded = dfile.read()

    with open(md5file, 'rb') as mfile:
        md5 = mfile.read()

    downloadedtomd5 = hashlib.md5(downloaded).digest()

    if downloadedtomd5 == md5:
        outLabel = Label(mGui, text='files are equal').grid(row=3, column=7, sticky=W)
    else:
        outLabel = Label(mGui, text='files are not equal').grid(row=3, column=7, sticky=W)

mGui = Tk()
ginputfile = StringVar()
goutputfile = StringVar()
gpassword = StringVar()
gkeyfile = StringVar()
gencfile = StringVar()
gkeyfile2 = StringVar()
gdecfile = StringVar()
gsourcefile = StringVar()
gdownloadedfile = StringVar()
gmd5hashfile = StringVar()

mGui.title('Encryption and Decryption')

Label0 = Label(text='File to encrypt:').grid(row=1,column=0,sticky=W)
Label1 = Label(text='Output file name:').grid(row=2,column=0, sticky=W)
Label2 = Label(text='Keyfile file name:').grid(row=3,column=0, sticky=W)
Label3 = Label(text='Password:').grid(row=4, column=0, sticky=W)

Label4 = Label(text='Encrypted file:').grid(row=1, column=2, sticky=W)
Label5 = Label(text='Keyfile:').grid(row=2, column=2, sticky=W)
Label6 = Label(text='Decrypted file name:').grid(row=3, column=2, sticky=W)

Label7 = Label(text='Source file:').grid(row=1, column=4, sticky=W)

Label8 = Label(text='Downloaded file:').grid(row=1, column=6, sticky=W)
Label9 = Label(text='md5 hash file:').grid(row=2, column=6, sticky=W)

encButton = Button(text='encrypt',command=encrypt).grid(row=0,column=0)
decButton = Button(text='decrypt',command=decrypt).grid(row=0,column=2)
md5Button = Button(text='produce md5',command=producemd5).grid(row=0,column=4)
md5Button2 = Button(text='check md5',command=checkmd5).grid(row=0,column=6)

Entry0 = Entry(mGui,textvariable=ginputfile).grid(row=1,column=1)
Entry1 = Entry(mGui,textvariable=goutputfile).grid(row=2,column=1)
Entry2 = Entry(mGui,textvariable=gkeyfile).grid(row=3,column=1)
Entry3 = Entry(mGui,textvariable=gpassword).grid(row=4,column=1)

Entry4 = Entry(mGui,textvariable=gencfile).grid(row=1,column=3)
Entry5 = Entry(mGui,textvariable=gkeyfile2).grid(row=2,column=3)
Entry6 = Entry(mGui,textvariable=gdecfile).grid(row=3,column=3)

Entry7 = Entry(mGui,textvariable=gsourcefile).grid(row=1,column=5)

Entry8 = Entry(mGui,textvariable=gdownloadedfile).grid(row=1,column=7)
Entry9 = Entry(mGui,textvariable=gmd5hashfile).grid(row=2,column=7)

mGui.mainloop()
