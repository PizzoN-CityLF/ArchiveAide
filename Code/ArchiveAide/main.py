#Outputting everything.
import argparse
import clp
import ocr
import tsa
import loc
import os

if __name__ == "__main__":
    rootPath = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='ArchiveAide')
    parser.add_argument('-clp', action = "store_true")
    parser.add_argument('-ocr', action = "store_true")
    parser.add_argument('-tsa', action = "store_true")
    parser.add_argument("-loc", action = "store_true")
    args = parser.parse_args()
    if (args.clp):
        print("Beginning Sort")
        clp.main(rootPath)
        print("Sort Completed")
    if (args.ocr):
        print("Initializing OCR")
        ocr.main(rootPath)
        print("OCR Completed")
    if (args.tsa):
        print("Initializing Summarizer")
        tsa.main(rootPath)
    if (args.loc):
        print("Adding to locator file")
        loc.main(rootPath)
        print("Completed adding to locator file")