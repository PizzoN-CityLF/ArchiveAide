# ArchiveAide

ArchiveAide is a program that is intended to massively speed up the process of converting physical documents to useful digital data. The program takes images of documents (Either just photos or scans from apps like Microsoft365 or iOS Notes), and a sorting configuration file, and creates a sorted file tree that includes PDFs of the images with 99+% Accurate backing text and AI-generated summaries of the data in those documents. This repository contains the code for **ArchiveAide**, which is responsible for all image processing of the project, and **ConfigWriter**, a program designed to create the configuration files that are used by ArchiveAide.

## Table of Contents

* [Archive Aide](#archiveaide)
  * [History](#history)
  * [Installation](#installation)
  * [Using ConfigWriter](#configwriter-usage)
  * [Using ArchiveAide](#archiveaide-usage)
  * [Tutorials](#tutorials)
  * [Support](#support)

## History

ArchiveAide and ConfigWriter were designed and developed by Nicholas Pizzo, an intern at the City Clerk's officer of the City of Lake Forest, Illinois, during the summer of 2024. The tools were designed to aid with the scanning and post-scanning usage of the tens of thousands of one-of-a-kind physical documents in the archives of the Lake Forest City Hall. Further thanks are required to City Clerk Margaret Boyer and Assistant City Manager George Issakoo for their support during the project's development.

## Installation 

ArchiveAide has several requirements that must be installed for the program to function
* [Python 3.8+](https://www.python.org/downloads/)
* [Tesseract-OCR 5.x](https://github.com/UB-Mannheim/tesseract/wiki)
* [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/) and [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) or [Standalone Microsoft Visual C++ Compiler](https://gist.github.com/mmozeiko/7f3162ec2988e81e56d5c4e22cde9977#file-portable-msvc-py)
* [Python Packages in Requirements.txt](requirements.txt)

*You may increase the speed of he summarizer by utilizing the CUDA system with a NVIDIA GPU. Use the following [Requirements File](requirements_with_CUDA.txt) instead*

Further, please note that Python and Tesseract must be added to your system's PATH, and if using the Standalone C++ Compiler, the extra files `libomp140.x86_64.dll` and `vcomp140.dll` must be added to your `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\lib` folder. 

ArchiveAide itself can be downloaded from the [Releases Page of this Repository](https://github.com/PizzoN-CityLF/ArchiveAide/releases)

**ArchiveAide.zip** includes both ConfigWriter and ArchiveAide, as well as .bat files to run the programs. 

**ArchiveAideFullInstall.zip** includes ConfigWriter, ArchiveAide, .bat files to run the programs, .exe files for all necessary dependencies, the standalone compiler, and a .bat file to set up the compiler and packages without further input.

The following are instructions for the installation process using the FullInstall.zip file. These Instructions are also followed in the [Tutorial Video](#tutorials)

1. Download and unzip `ArchiveAideFullInstall.zip`
2. In the dependencies folder, run the Python Installer exe. **Ensure that you check "Add Python to PATH" before installing**
3. In the dependencies folder, run the Tesseract Installer exe. No need to change any of the default options.
4. Open your windows Environment Variables. Edit the "Path" user variable, and add `C:\Users\USERNAME\AppData\Local\Programs\Tesseract-OCR`, changing `USERNAME` to your computer's Username.
5. In the dependencies/msvc folder, run `setup_x64.bat`. If you have Microsoft Visual Studio installed, the final copy commands may return errors, but they may be ignored.

## ConfigWriter Usage

There is also a video tutorial for ConfigWriter in the [Tutorials](#tutorials) tab

ConfigWriter is essentially a stripped-down texteditor created inside of Python Tkinter. Doubleclick the `RUN_ConfigWriter.bat` file to run the program. 

The difference between ConfigWriter and the simple Windows Notepad are that ConfigWriter is that ConfigWriter has built-in keybind macros that provide for easy creation of ArchiveAide Config Files (AACF)

Although you cannot save a file as .AACF, the format provides a easily readable and writable go-between to create a working .csv file to sort with. The format is read by splitting the entire file by whitespace, and by reading its "commands", which can either be 'Global' or 'Local'

Global Keywords edit which primary data structure the next 'Local' item will be in; The Global Keywords are as follows:
   * `Box` - Moves to the next "Box". The Box is the largest data structure of ArchiveAide. All items must be in a Box and Folder.
   * `Folder` - Moves to the next "Folder". The Folder is the secondary data structure of ArchiveAide. All items must be in a folder, which is in a box.
   * `Part` - Moves to the next "Part". The Part is the optional tertiary data structure of ArchiveAide. Parts do not change the tree structure, and are only extra data that can be used in other applications.
   * `End` - Ends the file. This is not automatically placed, and must be added by the user.

*Note:* All files should begin with `Box Folder` to ensure that the program is placing the first item into a Box and a Folder. If beginning in a part, `Box Folder Part` should open the file.

All files also have a local string, which is in the format:
`1 2 ... n-1 n Date #[#] #[#] #### [To ####]`, where n is the number of pages of that file.

The Local Keywords are as follows:
   * `1` - If not in a "Date Portion", signals the beginning of a new number
   * Number other than `1` - If the next item is "Date", signals the number of pages in the file. Otherwise, this data is extra and skipped.
   * `Date` - Signals the entrance into a three-word "Date Portion"; Format is Month Day Year, all integers.
   * `To` - Placed afterwards the year in a "Date Portion", to extend the portion by one more word to allow for approximate dating.
   * `None` - A keyword also valid for usage in a "Date Portion" instead of integers for when a Month, Date, or Year is unknown.

Both Global and Local Commands have macros. The following are the defaults but can be changed by going to Settings > "Set Keybinds"
   * `Control-b`:	`Box `
   * `slash`:	`Folder `
   * `Control-p`:	`Part `
   * `plus`:	`Date `
   * `asterisk`:	` To `
   * `minus`:	`None `
   * `Control-e`:	`End`
   * `period`:	` `


As an example of a full file, consider the .AACF Input:

`Box Folder Part 1 2 3 Date 1 12 1904 1 2 Date 5 15 1987 Part 1 2 Date 12 25 2022 To 2024 Folder 1 2 Date 4 26 2005 Box Folder 1 2 Date 8 9 1888 End`
 
The File Tree generated by the program will look like this.
 ```
 Box 1
  Folder 1
    Item 1.1.1 (Pages Number: 3 Part: A Date: 1/12/1904)
    Item 1.1.2 (Pages Number: 2 Part: A Date: 5/15/1987)
    Item 1.1.3 (Pages Number: 2 Part: B Date: 12/25/2022-2024)
  Folder 2
    Item 1.2.1 (Pages Number: 2 Date: 4/26/2005)
Box 2
  Folder 1
    Item 2.1.1 (Pages Number: 2 Date: 8/9/1888)
 ```

Once you have created your file, export it by going to Export Menu > "Open Export Dialogue".

Enter the number of the first box, folder, part, and item you scanned documents into.

Click "Save Settings and See Config Out", ensure that the result printed on the next page is correct, and click "Save in the IN folder of ArchiveAide"

Select the "in" folder of ArchiveAide in the file menu.

## ArchiveAide Usage

There is also a video tutorial for ArchiveAide in the [Tutorials](#tutorials) tab

Usage of ArchiveAide is relatively simple. Drag all images that were scanned into the ArchiveAide/in/photos folder. **Ensure they are in "Alphabetical Order"** (This will most likely already be the case depending on how you scanned the documents). Create the configuration .csv file from ConfigWriter and ensure that it is with the filename `./ArchiveAide/in/config/.csv`

Run the `RUN_ArchiveAide.bat` file, and enter one of the Config Options. The four options are:
   * `sort` - Which only creates the sorted file tree from config
   * `ocr` - Which only creates the sortable PDF documents from images
   * `summarize` - Which only creates the AI-Generated document summaries
   * `locator` - Which only adds the date and summary data to a main "locator" .csv file
   * `all` - Which does all four.

 **NOTE: Do NOT run OCR without running sort first, Do NOT run Summarize without running Sort and OCR First, Do NOT run locator without running Sort and Summarize first. It is highly recommended to use all unless you have a specific usecase preventing you from doing so.**

The output of ArchiveAide will be in `./ArchiveAide/out`

*Note: For Reading & Copying Data from PDFs directly, some programs (such as chrome's integrated PDF reader) are unsuccessful. Please use [Adobe's Free PDF Reader](https://get.adobe.com/reader/)*
## Tutorials

[Installing ArchiveAide from the Full Install]

[Using ConfigWriter]

[Using ArchiveAide]

## Support

Support and maintenance for this package is done by a single volunteer who is also a full-time student, and thus issues may take a long time to be resolved. Please check the [Tutorials](#tutorials) before posting a GitHub Issue.
