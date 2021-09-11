def download_wbt(verbose=False):
    """
    Download WhiteboxTools pre-complied binary for first-time use
    """
    import os, sys, platform
    import zipfile
    import tarfile
    import shutil
    import urllib.request
    import pkg_resources

    # print("Your operating system: {}".format(platform.system()))
    package_name = "whitebox"
    # Get package directory
    pkg_dir = os.path.dirname(
        pkg_resources.resource_filename(package_name, "whitebox_tools.py")
    )
    exe_dir = os.path.join(
        pkg_dir, "WBT"
    )  # Get directory of WhiteboxTools executable file
    work_dir = os.path.join(pkg_dir, "testdata")  # Set working directory
    init_img_dir = os.path.join(exe_dir, "img")
    new_img_dir = os.path.join(pkg_dir, "img")
    init_plugin_dir = os.path.join(exe_dir, "plugins")
    new_plugin_dir = os.path.join(pkg_dir, "plugins")

    links = {
        "Windows": "https://www.whiteboxgeo.com/WBT_Windows/WhiteboxTools_win_amd64.zip",
        "Darwin": "https://www.whiteboxgeo.com/WBT_Darwin/WhiteboxTools_darwin_amd64.zip",
        "Linux": "https://www.whiteboxgeo.com/WBT_Linux/WhiteboxTools_linux_amd64.zip",
    }

    # These are backup links only used to pass GitHub automated tests. WhiteboxGeo links frequently encourter timeout errors, which fail the automated tests.
    backup_links = {
        "Windows": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_win_amd64.zip",
        "Darwin": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_darwin_amd64.zip",
        "Linux": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_linux_amd64.zip",
    }

    try:

        if not os.path.exists(
            exe_dir
        ):  # Download WhiteboxTools executable file if non-existent
            if verbose:
                print(
                    "Downloading WhiteboxTools pre-compiled binary for first time use ..."
                )
            if platform.system() in links.keys():
                url = links[platform.system()]

            else:
                print(
                    "WhiteboxTools is not yet supported on {}!".format(
                        platform.system()
                    )
                )
                exit()

            zip_name = os.path.join(
                pkg_dir, os.path.basename(url)
            )  # Get WhiteboxTools zip file name
            zip_ext = os.path.splitext(zip_name)[1]  # Get downloaded zip file extension
            # urllib.request.urlretrieve(url, zip_name)   # Download WhiteboxTools
            try:
                request = urllib.request.urlopen(url, timeout=500)
            except urllib.error.URLError as e:
                print(e)
                print("Trying backup link ...")
                url = backup_links[platform.system()]
                request = urllib.request.urlopen(url, timeout=500)

            with open(zip_name, "wb") as f:
                f.write(request.read())

            if verbose:
                print("Decompressing {} ...".format(os.path.basename(url)))
            if zip_ext == ".zip":  # Decompress Windows/Mac OS zip file
                with zipfile.ZipFile(zip_name, "r") as zip_ref:
                    zip_ref.extractall(pkg_dir)
            else:  # Decompress Linux tar file
                with tarfile.open(zip_name, "r") as tar_ref:
                    tar_ref.extractall(pkg_dir)
            if verbose:
                print("WhiteboxTools package directory: {}".format(pkg_dir))

            if os.path.exists(new_img_dir):
                shutil.rmtree(new_img_dir)
            if os.path.exists(new_plugin_dir):
                shutil.rmtree(new_plugin_dir)

            shutil.copytree(init_img_dir, new_img_dir)
            shutil.copytree(init_plugin_dir, new_plugin_dir)

            exe_ext = ""  # file extension for MacOS/Linux
            if platform.system() == "Windows":
                exe_ext = ".exe"
            exe_name = "whitebox_tools{}".format(exe_ext)
            exe_path = os.path.join(exe_dir, exe_name)

            if platform.system() != "Windows":  # grant executable permission
                os.system("chmod 755 " + exe_path)

            exe_path_new = os.path.join(pkg_dir, exe_name)
            shutil.copy(exe_path, exe_path_new)

        if not os.path.exists(work_dir):
            if verbose:
                print("Downloading testdata ...")
            os.mkdir(work_dir)
            dem_url = "https://github.com/giswqs/whitebox-python/raw/master/examples/testdata/DEM.tif"
            dep_url = "https://github.com/giswqs/whitebox-python/raw/master/examples/testdata/DEM.dep"
            urllib.request.urlretrieve(dem_url, os.path.join(work_dir, "DEM.tif"))
            urllib.request.urlretrieve(dep_url, os.path.join(work_dir, "DEM.dep"))

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


if __name__ == "__main__":
    download_wbt()
