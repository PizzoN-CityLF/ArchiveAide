from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.geometry("1200x660")
root.title("ArchiveAide TextEditor")
rootPath = os.path.dirname(os.path.realpath(__file__))
frame = Frame(root)
frame.pack(pady=5)
curr = None

keybinds = {}
with open(rootPath + "/base/settings.csv", 'r', encoding="utf-8") as f:
    parts = f.read().split("\n")
    for part in parts:
        p = part.split(",")
        keybinds[p[0]] = p[1]

binds = []

isInDate = False

def new_file():
    text.delete("1.0", END)

def open_file():
    text.delete("1.0", END)
    textFile = filedialog.askopenfilename(initialdir=rootPath, title="Open File", filetypes=[("Text Files", "*.txt")])
    with open(textFile, 'r', encoding="utf-8") as f:
        data = f.read()
        text.insert(END, data)

def open_saved_file():
    text.delete("1.0", END)
    with open(rootPath + '/base/saved.txt', 'r', encoding="utf-8") as f:
        data = f.read()
        text.insert(END, data)

def export_file():
    textFile = filedialog.asksaveasfile(defaultextension=".txt", initialdir=rootPath, title="Save File", filetypes=[("Text Files", "*.txt")])
    if textFile:
        with open(textFile.name, "w", encoding="utf-8") as f:
            f.write(text.get(1.0, END))
        
def save_file():
    with open(rootPath + "\\base\\saved.txt", "w", encoding="utf-8") as f:
        f.write(text.get(1.0, END))

def change_text(info):
    keybindName = event_to_keytext(info)
    if info.state & 4:
        text.insert(text.index(INSERT), keybinds[keybindName])
    else:
        text.replace(text.index("insert-1c"), text.index(INSERT), keybinds[keybindName])

def num_change_text(info):
    global isInDate
    seen = 0
    i = 1
    while (f'1.{i}' != text.index(INSERT) and seen < 5):
        if (text.get(text.index(f'insert-{i+1}c'), text.index(f'insert-{i}c')) == " "):
            seen = seen + 1
        i = i+1
    arr = text.get(text.index(f'insert-{i-1}c'), text.index(INSERT)).split(" ")
    expand = True
    if isInDate:
        if arr[0] == "Date" or arr[2] == "To":
            isInDate = False
            text.insert(text.index(INSERT), " ")
    elif arr[-2].isnumeric():
        for i in range(len(arr[-2])):
            if arr[-2][i] != "9":
                expand = False
                break
        if (expand):
            if (len(arr[-2]) + 1 == len(arr[-1])):
                text.insert(text.index(INSERT), " ")
        else:
            if (len(arr[-2]) == len(arr[-1])):
                text.insert(text.index(INSERT), " ")
    elif arr[-2] == "Date":
        save_file()
        isInDate = True
    else:
        text.insert(text.index(INSERT), " ")
    
    #check with date

def event_to_keytext(event):
    keys = []
    if event.state & 1:
        keys.append("Shift")
    if event.state & 4:
        keys.append("Control")
    keys.append(event.keysym)
    return "-".join(keys)

def buttonInput(popup, name, num):
    init_names = ("Box   ", "Folder", "Part  ", "Date  ", "To    ", "None  ", "End   ", "Space ")
    global curr
    b = popup.nametowidget("mf." + name)
    if (b["text"] != "Click again to save!"):
        b.config(text="Click again to save!")
        curr = popup.nametowidget("mf." + name.replace("B", "T"))
    else:
        b.config(text=init_names[num-1])
        curr = None
    
def unbind_all():
    for i, key in enumerate(keybinds):
        root.unbind(key, binds[i])

def keybinds_to_file():
    str = ""
    for key, value in keybinds.items():
        str += key + "," + value + "\n"
    str = str[:-1]
    with open(rootPath + "/base/settings.csv", "w", encoding="utf-8") as f:
        f.write(str)

def set_keybinds():
    def keybind_handler(event):
        global curr
        if curr is not None:
            curr.config(state=NORMAL)
            curr.replace(1.0, END, event_to_keytext(event))
            curr.config(state=DISABLED)
    popup = Tk()
    popup.geometry("600x330")
    popup.title("Keybind Selector")
    mainFrame = Frame(popup, name="mf")
    mainFrame.pack()
    currentBinds = list(keybinds.keys())
    Button(mainFrame, text = "Box   ", name="boxB", command=lambda:buttonInput(popup,"boxB",1)).grid(row = 0, column = 0, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "Folder", name="folderB", command=lambda:buttonInput(popup,"folderB",2)).grid(row = 1, column = 0, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "Part  ", name="partB", command=lambda:buttonInput(popup,"partB",3)).grid(row = 2, column = 0, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "Date  ", name="dateB", command=lambda:buttonInput(popup,"dateB",4)).grid(row = 3, column = 0, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "To    ", name="toB", command=lambda:buttonInput(popup,"toB",5)).grid(row = 0, column = 2, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "None  ", name="noneB", command=lambda:buttonInput(popup,"noneB",6)).grid(row = 1, column = 2, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "End   ", name="endB", command=lambda:buttonInput(popup,"endB",7)).grid(row = 2, column = 2, sticky = W, pady = 2, padx=10)
    Button(mainFrame, text = "Space ", name="spaceB", command=lambda:buttonInput(popup,"spaceB",8)).grid(row = 3, column = 2, sticky = W, pady = 2, padx=10)
    Text(mainFrame, name="boxT", width=25, height=2).grid(row=0, column=1, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="folderT", width=25, height=2).grid(row=1, column=1, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="partT", width=25, height=2).grid(row=2, column=1, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="dateT", width=25, height=2).grid(row=3, column=1, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="toT", width=25, height=2).grid(row=0, column=3, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="noneT", width=25, height=2).grid(row=1, column=3, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="endT", width=25, height=2).grid(row=2, column=3, sticky=W, pady=2, padx=5)
    Text(mainFrame, name="spaceT", width=25, height=2).grid(row=3, column=3, sticky=W, pady=2, padx=5)
    for bind in currentBinds:
        widget = None
        if (keybinds[bind] == " "):
            widget = popup.nametowidget("mf.spaceT")
        else:
            widget = popup.nametowidget("mf." + keybinds[bind].replace(" ", "").lower() + "T")
        widget.insert(1.0, bind)
        widget.config(state=DISABLED)
    popup.bind("<Key>", keybind_handler)
    def save_settings():
        global keybinds
        newDict = {}
        for bind in currentBinds:
            widget = None
            if (keybinds[bind] == " "):
                widget = popup.nametowidget("mf.spaceT")
            else:
                widget = popup.nametowidget("mf." + keybinds[bind].replace(" ", "").lower() + "T")
            newDict[widget.get(1.0, END).replace("\n", "")] = keybinds[bind]
        unbind_all()
        keybinds = newDict
        base_keybinds()
        keybinds_to_file()
        popup.destroy()
    Button(mainFrame, text = "Save Settings",command=save_settings).grid(row = 5, column = 0, sticky = W, pady = 30, padx=10)
    Button(mainFrame, text = "Cancel", command=popup.destroy).grid(row = 5, column = 2, sticky = W, pady = 30, padx=10)

def base_keybinds():
    global binds
    binds = []
    for key in keybinds:
        binding = root.bind(f'<{key}>', change_text)
        binds.append(binding)
    for i in range(10):
        binding = root.bind(f'<Key-{i}>', num_change_text)
        binds.append(binding)

def addSavedStr(saved, np):
    if np != 0:
        with open(rootPath + "/result.csv", "a") as f:
           f.write(saved.replace(" ", ",") + "," + str(np) + "\n")

def commands_CLP(data_clp, boxin, folderin, partin, itemin):
    i = 0
    start = False
    if (folderin != 1 or (partin != "" and partin != "A") or itemin != 1):
        start = True
    box = boxin-1
    folder = folderin-1
    part = "" if partin == " " or partin == "A" else chr(ord(partin) - 1)
    item = itemin-1
    num_pages = 0
    saved = ""
    while i < len(data_clp):
        curr = data_clp[i]
        if curr == "box":
            box += 1
            if not start:
                folder = 0
                part = ""
                item = 0
        elif curr == "folder":
            folder += 1
            if not start:
                part = ""
                item = 0
            start = False
        elif curr == "part":
            if part == "":
                part = "A"
            else:
                part = chr(ord(part) + 1)
        elif curr == "1":
            addSavedStr(saved, num_pages)
            saved = ""
            item += 1
            num_pages = 1
        elif curr.isnumeric():
            num_pages = int(curr)
        elif curr == "date":
            saved += (
                str(box)
                + " "
                + str(folder)
                + " "
                + ("-" if part == "" else part)
                + " "
                + str(item)
                + " "
                + data_clp[i + 1]
                + " "
                + data_clp[i + 2].replace("st", "").replace("nd", "").replace("th", "")
            )
            if data_clp[i + 4] == "to":
                saved += " - " + data_clp[i + 3] + " " + data_clp[i + 5]
                i += 5
            else:
                saved += " " + data_clp[i + 3] + " - -"
                i += 3
        elif curr == "end":
            addSavedStr(saved, num_pages)
            break
        else:
            print("err! " + curr)
        i += 1

def getTextData():
    with open(rootPath + "/result.csv", "r", encoding="utf-8") as f:
        data = f.readlines()
    data.pop(0)
    currBox = 0
    currFolder = 0
    strOut = ""
    for line in data:
        line = line.replace("\n", "").split(",")
        if (line[0] != currBox):
            strOut += "Box " + line[0] + "\n"
            currBox = line[0]
        if (line[1] != currFolder):
            strOut += "  Folder " + line[1] + "\n"
            currFolder = line[1]
        strOut += "    Item " + line[0] + "." + line[1] + "." + line[3] + " (Pages Number: " + line[-1]
        if (line[2] != "-"):
            strOut += " Part: " + line[2]
        if (line[6] != "-"):
            strOut += " Date: " + line[4] + "/" + line[5] + "/" + line[6] + ")\n"
        else:
            strOut += " Date: " + line[4] + "/" + line[5] + "/" + line[7] + "-" + line[8] + ")\n"
    return strOut

def save_file_specific(popup):
    dir = filedialog.askdirectory(initialdir=rootPath)
    os.replace(rootPath + "/result.csv", dir + "/config.csv")
    root.quit()

def config_page():
    popup = Tk()
    popup.geometry("1000x550")
    mainFrame = Frame(popup, name="mf")
    mainFrame.pack()
    Label(mainFrame, text = "Below is the result of the config file you inputted.", font=("Helvetica", 16)).grid(row=0,column=0,sticky=W,columnspan=2)
    textbox = Text(mainFrame)
    textbox.grid(row=1,column=0,sticky=W,columnspan=2)
    Button(mainFrame, command=popup.destroy, text="Exit", width=32, height=2, font=("Helvetica", 12)).grid(row=2,column=0,sticky=W, pady=15)
    Button(mainFrame, command=lambda:save_file_specific(popup), text="Save in the IN folder of ArchiveAide", width=32, height=2, font=("Helvetica", 12)).grid(row=2,column=1,sticky=E, pady=15)
    textData = getTextData()
    textbox.insert(1.0, textData)
    scroll = Scrollbar(mainFrame, command=textbox.yview)
    scroll.grid(row=1, column=2, sticky='ns')
    textbox.config(yscrollcommand=scroll.set)
    textbox.config(state="disabled")

def outward_file():
    def show_config_file():
        arr = None
        with open(rootPath + "/base/saved.txt", "r", encoding="utf-8") as f:
            arr = f.read().lower().split()
        error_msg = ""
        data = (popup.nametowidget("mf.box").get(1.0, END).replace("\n", ""), popup.nametowidget("mf.folder").get(1.0, END).replace("\n", ""), popup.nametowidget("mf.part").get(1.0, END).replace("\n", ""), popup.nametowidget("mf.item").get(1.0, END).replace("\n", ""))
        if not data[0].isnumeric():
            error_msg += "Box must be number! "
        if not data[1].isnumeric():
            error_msg += "Folder must be number! "
        if data[2] != " " and (not len(data[2]) == 1 or not data[2][0].isalpha()):
            error_msg += "Part must be single letter or space! "
        if not data[3].isnumeric():
            error_msg += "Item must be number!"
        if (error_msg != ""):
            error_label.config(text=error_msg)
        else:
            commands_CLP(arr, int(data[0]), int(data[1]), data[2], int(data[3]))
            popup.destroy()
            config_page()
    if os.path.isfile(rootPath + "/result.csv"):
        os.unlink(rootPath + "/result.csv")
    with open(rootPath + "/result.csv", "a") as f:
        f.write("box,folder,part,item,month,day,year,year_start,year_end,num_pages\n")
    currText = text.get(1.0, END)
    with open(rootPath + "\\base\\saved.txt", "w", encoding="utf-8") as f:
        f.write(currText)
    arr = currText.lower().split()
    popup = Tk()
    popup.geometry("800x330")
    popup.title("Export Dialogue")
    mainFrame = Frame(popup, name="mf")
    mainFrame.pack()
    Label(mainFrame, text = "Box", font=("Helvetica", 16)).grid(row=0, column=0, sticky=W)
    Label(mainFrame, text = "Folder", font=("Helvetica", 16)).grid(row=1, column=0, sticky=W)
    Label(mainFrame, text = "Part", font=("Helvetica", 16)).grid(row=2, column=0, sticky=W)
    Label(mainFrame, text = "Item", font=("Helvetica", 16)).grid(row=3, column=0, sticky=W)
    btext = Text(mainFrame, height=1, width=5, name = "box")
    btext.insert(1.0, "1")
    btext.grid(row=0, column=1, sticky=W)
    ftext = Text(mainFrame, height=1, width=5, name = "folder")
    ftext.insert(1.0, "1")
    ftext.grid(row=1, column=1, sticky=W)
    ptext = Text(mainFrame, height=1, width=5, name = "part")
    ptext.insert(1.0, " ")
    ptext.grid(row=2, column=1, sticky=W)
    itext = Text(mainFrame, height=1, width=5, name = "item")
    itext.insert(1.0, "1")
    itext.grid(row=3, column=1, sticky=W)
    Label(mainFrame, text = "Enter the number of the first box you scanned items from", font=("Helvetica", 11)).grid(row=0, column=2, sticky=W, pady=10, padx=3)
    Label(mainFrame, text = "Enter the number of the first folder you scanned items from", font=("Helvetica", 11)).grid(row=1, column=2, sticky=W, pady=10, padx=3)
    Label(mainFrame, text = "If starting within a folder and within a part, enter the letter for the first part\nyou scanned items from. Else, leave blank", font=("Helvetica", 11), justify=LEFT).grid(row=2, column=2, sticky=W, pady=10, padx=3)
    Label(mainFrame, text = "if starting from within a folder, enter the item number of the first item that\nyou scanned. Else, leave 1", font=("Helvetica", 11), justify=LEFT).grid(row=3, column=2, sticky=W, pady=10, padx=3)
    error_label = Label(mainFrame, text = "", font = ("Helvetica", 11), fg="red")
    error_label.grid(row=4, column=0, columnspan=2)
    Button(mainFrame, text = "Save Settings and See Config Out", command=show_config_file).grid(row=5, column=0, columnspan=2)

text_scroll = Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)

text = Text(frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
text.pack()

text_scroll.config(command=text.yview)

mainMenu = Menu(root)
root.config(menu=mainMenu)

fileMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=new_file)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Open From Save", command=open_saved_file)
fileMenu.add_command(label="Save", command=save_file)
fileMenu.add_command(label="Save As", command=export_file)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
editMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="Settings", menu=editMenu)
editMenu.add_command(label="Set Keybinds", command=set_keybinds)
configMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="Export Menu", menu=configMenu)
configMenu.add_command(label="Open Export Dialogue", command=outward_file)


base_keybinds()

root.mainloop()
