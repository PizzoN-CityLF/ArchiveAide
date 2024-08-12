import os

def getDirs(root):
    dirs = []
    for dir in os.listdir(root + "/out"):
        if dir[-4:] != ".csv":
            for dir2 in os.listdir(root + "/out/" + dir):
                for dir3 in os.listdir(root + "/out/" + dir + "/" + dir2):
                    dirs.append(root + "/out/" + dir + "/" + dir2 + "/" + dir3)
    return dirs

def main(root):
    dirs = getDirs(root)
    add = ""
    cfg = ""
    with open(f"{root}/in/config.csv", "r", encoding="utf-8") as f:
        cfg = f.read().strip()
    cfg = cfg.split()[1:]
    cfg2 = []
    for line in cfg:
        cfg2.append(line[:line.rfind(",")])
    cfg = cfg2
    print(cfg)
    for i, dir in enumerate(dirs):
        with open(dir + "/summary.txt", "r", encoding="utf-8") as f:
            add = add + cfg[i] + "," + "\"" + f.read() + "\"\n"
    with open(root + "/out/locator.csv", "a", encoding="utf-8") as f:
        f.write(add)