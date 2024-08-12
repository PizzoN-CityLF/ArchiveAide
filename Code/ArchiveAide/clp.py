import os

def main(root):
    outdir = root + "/out/"
    with open(root + "/in/config.csv", encoding="utf-8") as f:
        data = f.readlines()
    data.pop(0)
    photos = os.listdir(root + "/in/photos")
    photos.reverse()
    currBox = 0
    currFolder = 0
    for line in data:
        line = line.split(",")
        box = line[0]
        folder = line[1]
        item = line[3]
        num_pages = int(line[-1].replace("\n", ""))
        if (currBox != box):
            try:
                os.mkdir(outdir + "Box " + box)
            except FileExistsError:
                pass
            currBox = box
            currFolder = 0
        if (currFolder != folder):
            try:
                os.mkdir(outdir + "Box " + box + "/Folder " + folder)
            except FileExistsError:
                pass
            currFolder = folder
        dirname = outdir + "Box " + box + "/Folder " + folder + "/" + box + "." + folder + "." + item
        try:
            os.mkdir(dirname)
        except FileExistsError:
            pass
        for i in range(num_pages):
            fname = photos.pop()
            os.replace(root + "/in/photos/" + fname, dirname + "/" + str(i + 1) + ".JPG")

