# ArchiveAide

ArchiveAide is a program that is intended to massively speed up the process of converting physical documents to useful digital data. The program takes images of documents (Either just photos or scans from apps like Microsoft365 or iOS Notes), and a sorting configuration file, and creates a sorted file tree that includes PDFs of the images with 99+% Accurate backing text and AI-generated summaries of the data in those documents. 

## Table of Contents

* [Archive Aide](#archiveaide)
  * [History](#history)
  * [Installation](#installation)
  * [Using ConfigWriter](#configwriter-usage)
  * [Using ArchiveAide](#archiveaide-usage)
  * [Tutorials](#tutorials)
  * [Support](#support)

## History

ArchiveAide and ConfigWriter were designed and developed by Nicholas Pizzo, an intern at the City Clerk's officer of the City of Lake Forest, Illinois, during the summer of 2024. The tools were designed to aid with the scanning and post-scanning usage of the tens of thousands of one-of-a-kind physical documents in the archives of the Lake Forest City Hall. Further thanks are required to City Clerk Margaret Boyer and Assistant City Manager George Issakoo for their support during the project's creation.

## Installation 

ArchiveAide has several requirements that must be installed for the program to function
* [Python 3.8+](https://www.python.org/downloads/)
* [Tesseract-OCR 5.x](https://github.com/UB-Mannheim/tesseract/wiki)
* [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/) and [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) or [Standalone Microsoft Visual C++ Compiler](https://gist.github.com/mmozeiko/7f3162ec2988e81e56d5c4e22cde9977#file-portable-msvc-py)
* [Python Packages in Requirements.txt](requirements.txt)

Further, please note that Python and Tesseract must be added to your system's PATH, and if using the Standalone C++ Compiler, the extra files `libomp140.x86_64.dll` and `vcomp140.dll` must be added to your `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\lib` folder. 

ArchiveAide itself can be downloaded from the [Releases] Page.

**ArchiveAideStandalone.zip** includes both ConfigWriter and ArchiveAide, as well as .bat files to run the programs.

**ArchiveAideFullInstall.zip** includes ConfigWriter, ArchiveAide, .bat files to run the programs, .exe files for all necessary dependencies, the standalone compiler, and a .bat file to set up the compiler and packages without further input.

The following are instructions for the installation process using the FullInstall.zip file. These Instructions are also followed in the [Tutorial Video](#tutorials)

1. Download and unzip `ArchiveAideFullInstall.zip`
2. In the dependencies folder, run the Python Installer exe. **Ensure that you check "Add Python to PATH" before installing**
3. In the dependencies folder, run the Tesseract Installer exe. No need to change any of the default options.
4. Open your windows Environment Variables. Edit the "Path" user variable, and add `C:\Users\USERNAME\AppData\Local\Programs\Tesseract-OCR`, changing `USERNAME` to your computer's Username.
5. In the dependencies/msvc folder, run `setup_x64.bat`. If you have Microsoft Visual Studio installed, the final copy commands may return errors, but they may be ignored.

## ConfigWriter Usage

There is also a tutorial for ConfigWriter in the [Tutorials](#tutorials) tab

## ArchiveAide Usage

There is also a tutorial for ArchiveAide in the [Tutorials](#tutorials) tab

## Tutorials

[Installing ArchiveAide from the Full Install]

[Using ConfigWriter]

[Using ArchiveAide]

## Support

Support and maintenance for this package is done by a single volunteer who is also a full-time student, and thus issues may take a long time to be resolved. Please check the [Tutorials](#tutorials) before posting a GitHub Issue.
