import os
import pytesseract
from symspellpy import SymSpell, Verbosity
import hocr_pdf as ocrpdf
import re

b = False

def progress_bar(current, total, bar_length=10):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'OCR Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def getDirs(root):
    dirs = []
    for dir in os.listdir(root + "/out"):
        if dir[-4:] != ".csv":
            for dir2 in os.listdir(root + "/out/" + dir):
                for dir3 in os.listdir(root + "/out/" + dir + "/" + dir2):
                    dirs.append(root + "/out/" + dir + "/" + dir2 + "/" + dir3)
    return dirs

def spellCheckHelper(str, str2):
    # if more than half capital
    if sum(1 for c in str2 if c.isupper()) > len(str) / 2:
        str = str.upper()
    # if first letter is capitalized
    elif str2[0].isupper():
        str = str.capitalize()
    # re add ; . , ? ! ' " at end
    if str2[-1].isalnum() or str2[-1] == "-":
        pass
    else:
        last = len(str2) - 1
        while last > 0:
            if str2[last].isalnum():
                break
            else:
                last = last - 1
        str = str + str2[last + 1 :]
    # re add ' " at beginning
    if str2[0] == '"' or str2[0] == "'" or str2[0] == "(":
        str = str2[0] + str
    return str


def spellCheck(word, sym_spell):
    global b
    simple = word.lower()
    if simple == "a" or simple == "i":
        return word
    word = word.replace("“", '"')
    word = word.replace("”", '"')
    word = word.replace("‘", "'")
    word = word.replace("’", "'")
    if word[-1:] == "+":
        word = word[:-1] + "-"
    word.replace("\n", " ")
    initialStr = word
    pattern = re.compile("[^a-z0-9- ]+")
    word = pattern.sub("", word.replace("\n", " ").lower())
    if (len(word) == 1 and len(initialStr) >= 2 and initialStr[1] == "."):
        return spellCheckHelper(word, initialStr)
    if word == "" and initialStr != "":
        return initialStr
    if word == "" and initialStr == "":
        pass
    elif word[len(word) - 1] == "-":
        b = True
    elif b:
        b = False
    else:
        suggestions = sym_spell.lookup(
            word, Verbosity.CLOSEST, max_edit_distance=2, transfer_casing=True
        )
        if len(suggestions) != 0:
            word = suggestions[0].term
    if word.isnumeric() or (len(word) == 2 and word[1] == "."):
        return spellCheckHelper(word, initialStr)
    if word == "" or (len(word) == 1 and (word != "a" or word != "i")):
        return ""
    return spellCheckHelper(word, initialStr)

def main(root):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    sym_spell.load_dictionary(
        root + "/data/frequency_dictionary_en_82_765.txt", term_index=0, count_index=1
    )
    print("OCR Initialized")
    dirs = getDirs(root)
    total = len(dirs)
    for num, dir in enumerate(dirs):
        files = os.listdir(dir)
        hOCRs = []
        for file in files:
            if file.endswith(".JPG"):
                with open(dir + "/" + file.replace(".JPG", ".hocr"), "w+b") as f:
                    data = pytesseract.image_to_pdf_or_hocr(dir + "/" + file, extension="hocr")
                    hOCRs.append(data)
                    f.write(data)
        textData = ""
        for i, ocr in enumerate(hOCRs):
            hocrData = b""
            for line in ocr.split(b"\n"):
                if (line.find(b"<span class='ocrx_word'") != -1):
                    lb = line[:-1].rfind(b">") + 1
                    rb = line.rfind(b"<")
                    word = line[lb:rb].decode("utf-8")
                    spcWord = spellCheck(word, sym_spell)
                    if word != spcWord:
                        newline = line[:lb] + spcWord.encode("utf-8") + line[rb:]
                        hocrData += newline + b"\n"
                    else:
                        hocrData += line + b"\n"
                    textData += spcWord + " "
                elif (line.find(b"<span class='ocr_line'") != -1):
                    textData += "\n"
                    hocrData += line + b"\n"
                else:
                    hocrData += line + b"\n"
            with open(dir + "/" + str(i+1) + ".hocr", "w+b") as f:
                f.write(hocrData)
            textData += "\n"
        with open(dir + "/text.txt", "w", encoding="utf-8") as f:
            f.write(textData.strip())
        ocrpdf.main(dir, dir + "/main.pdf")
        for file in files:
            if file.endswith(".JPG"):
                os.unlink(dir + "/" + file.replace(".JPG", ".hocr"))
        progress_bar((num+1), total)
