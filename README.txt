To Encrypt a File:
--have encrypt.py and file to be encrypted in the same directory
--run python encrypt.py <file to be encrypted> <encrypted output file name> <password> <keyfile file name>
--example
	$python encrypt.py message.txt encoded.enc examplepassword keyfile.enc

this will write encoded.enc (the encoded file) and keyfile.enc (the key) into the directory


To Decrypt a File:
--have decrypt.py, file to be decrypted, and keyfile in the same directory
--run python decrypt.py <encoded file> <keyfile> <decoded file name>
--example
	$python decrypt.py encoded.enc keyfile.enc decoded.txt

this will write decoded into the directory, but just as a file without the ending .txt
but if changed to .txt or opened with notepad++ or something it will display the correct
decoded text

should work with all file types
the decryptor needs to know the file type in order to change it and use the file