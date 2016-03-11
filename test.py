import keyring
import win32api

keyring.set_password("system","lap089","laplfsdklf")
lap = keyring.get_password("system","lap089")
print(lap)

file = open("lap089","w")
print(file.writelines("trieu quoc lap"))

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
print(drives)