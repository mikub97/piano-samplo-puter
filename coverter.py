import os

def convert(dir = "samples/fav/"):
    print(os.listdir(dir))
    for filename in os.listdir(dir):
        if ".wav" in filename:
            os.system("oggenc -q 3 -o " +dir+filename.split(".")[0]+".ogg"+" "+dir+filename.split(".")[0]+".wav")

    os.system("mkdir "+dir+"waves")
    os.system("mv "+dir+"*.wav "+dir+"waves")

