#!/usr/bin/env python
'''
This module automates the process for downloading WhiteboxTools library and testdata.
Only works for Python 3.x
Source: http://www.uoguelph.ca/~hydrogeo/WhiteboxTools/
GitHub: https://github.com/jblindsay/whitebox-tools
'''

import os
import sys
import platform
import zipfile
import tarfile
import shutil
import urllib.request


# Download WhiteboxTools pre-compiled binary
def download_wbt():
    print("Your operating system: {}".format(platform.system()))

    root_dir = os.path.dirname(os.path.abspath(__file__))   # Get root directory of the project
    exe_dir = os.path.join(root_dir, "WBT")                 # Get directory of WhiteboxTools executable file
    # src_dir = os.path.join(root_dir, "target/release/")     # Get directory of WhiteboxTools compiled from source
    work_dir = os.path.join(root_dir, "testdata")           # Set working directory

    try:
        # if os.path.exists(src_dir):     # check existence of WhiteboxTools compiled from source code
        #     exe_dir = src_dir
        if not os.path.exists(exe_dir):  # Download WhiteboxTools executable file if non-existent
            print("Downloading WhiteboxTools pre-compiled binary ...")
            if platform.system() == "Windows":
                # url = "http://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_win_amd64.zip"
                url = "http://spatial.binghamton.edu/download/whitebox/WhiteboxTools_win_amd64.zip"
            elif platform.system() == "Darwin":
                # url = "http://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_darwin_amd64.zip"
                url = "http://spatial.binghamton.edu/download/whitebox/WhiteboxTools_darwin_amd64.zip"
            elif platform.system() == "Linux":
                # url = "http://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_linux_amd64.tar.xz"
                url = "http://spatial.binghamton.edu/download/whitebox/WhiteboxTools_linux_amd64.tar.xz"
            else:
                print("WhiteboxTools is not yet supported on {}!".format(platform.system()))
                exit()

            zip_name = os.path.basename(url)            # Get WhiteboxTools zip file name
            urllib.request.urlretrieve(url, zip_name)   # Download WhiteboxTools
            zip_ext = os.path.splitext(zip_name)[1]     # Get downloaded zip file extension

            print("Decompressing downloaded file ...")
            if zip_ext == ".zip":       # Decompress Windows/Mac OS zip file
                with zipfile.ZipFile(zip_name, "r") as zip_ref:
                    zip_ref.extractall('.')
            else:                       # Decompress Linux tar file
                with tarfile.open(zip_name, "r") as tar_ref:
                    tar_ref.extractall('.')

        exe_ext = ""
        if platform.system() == 'Windows':
            exe_ext = '.exe'
        exe_name = "whitebox_tools{}".format(exe_ext)
        exe_path = os.path.join(exe_dir, exe_name)
        exe_path_new = os.path.join(root_dir, exe_name)
        print(exe_path)
        shutil.copy(exe_path, exe_path_new)

        if not os.path.exists(work_dir):
            print("Downloading testdata ...")
            os.mkdir(work_dir)
            dem_url = "https://github.com/jblindsay/whitebox-tools/raw/master/testdata/DEM.tif"
            dep_url = "https://github.com/jblindsay/whitebox-tools/raw/master/testdata/DEM.dep"
            urllib.request.urlretrieve(dem_url, "testdata/DEM.tif")
            urllib.request.urlretrieve(dep_url, "testdata/DEM.dep")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    print("WhiteboxTools executable file is located in: {}".format(exe_dir))


if __name__ == '__main__':

    download_wbt()


