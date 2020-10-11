import requests
import time

#Setting First Bin
r = requests.post("Place your create url here", data = {"name": "Ayman's Bin","description": "this bin belong to Ayman" })
time.sleep(8)
#Setting Second Bin
r = requests.post("Place your create url here", data = {"name": "Kandari's Bin","description": "this bin belong to Kandari" })
time.sleep(8)
#Setting Third Bin
r = requests.post("Place your create url here", data = {"name": "Mohammed's Bin","description": "this bin belong to Mohammed" })
time.sleep(8)
#Setting Fourth Bin
r = requests.post("Place your create url here", data = {"name": "Enezi's Bin","description": "this bin belong to Enezi" })
time.sleep(8)

print("Trash Bins Ready")





