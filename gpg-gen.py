import os
import gnupg
import subprocess

gpg = gnupg.GPG()

#User input
print('Please fill following Fields.')
print("-----------------------------------------------------------------")
mName = input("Name: ")
mEmail = input("E-Mail: ")
keyServerAdress = 'KeyServerAdress'
print("-----------------------------------------------------------------")

#Genereting PGP Cert
input_data = gpg.gen_key_input(
    key_type ='RSA',
    key_length=4096,
    key_usage='encrypt, sign',
    subkey_type='RSA',
    subkey_length= 4096,
    subkey_usage='encrypt',
    keyserver= keyServerAdress,
    name_comment='TEXT',
 	expire_date = 0,
    name_real= mName,
    name_email=mEmail,
    passphrase='PASS')
key = gpg.gen_key(input_data)

#Publish and check on server side
gpg.send_keys(keyServerAdress, key.fingerprint)

#dummy publish check
print("PGP Data Output. if [] cert wasnt publish")
print("-----------------------------------------------------------------")
print(gpg.search_keys(mEmail, keyServerAdress))
print("-----------------------------------------------------------------")

#Export Private Key
ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
ascii_armored_private_keys = gpg.export_keys(
    keyids=key.fingerprint,
    secret=True,
    passphrase='PASS',
)

keyFileNameMitKuerzel = mEmail + ".asc"

#Copy file to User NetworkShare Folder and to Admins Backup
with open(keyFileNameMitKuerzel, 'w') as f:
    f.write(ascii_armored_public_keys)
    f.write(ascii_armored_private_keys)

print("Job's Done. © Peasant ")
print("-----------------------------------------------------------------")
