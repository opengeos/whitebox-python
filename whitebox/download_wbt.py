def download_wbt(linux_musl=False, reset=False, verbose=True):
    """Downloads WhiteboxTools pre-complied binary for first-time use

    Args:
        linux_musl (bool, optional): Whether to download the musl version of WhiteboxTools for Linux. Defaults to False.
        reset (bool, optional): Whether to reset the WhiteboxTools installation. Defaults to False.
        verbose (bool, optional): Whether to print verbose messages. Defaults to True.
   
    """
    import glob
    import os
    import sys
    import platform
    import zipfile
    import tarfile
    import shutil
    import urllib.request
    import pkg_resources
    import webbrowser

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
        "Linux-musl": "https://www.whiteboxgeo.com/WBT_Linux/WhiteboxTools_linux_musl.zip"
    }

    if linux_musl or ('google.colab' in sys.modules) or (os.environ.get('WBT_LINUX', False) == "MUSL"):
        links["Linux"] = links["Linux-musl"]

    # These are backup links only used to pass GitHub automated tests. WhiteboxGeo links frequently encounter timeout errors, which fail the automated tests.
    backup_links = {
        "Windows": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_win_amd64.zip",
        "Darwin": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_darwin_amd64.zip",
        "Linux": "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_linux_amd64.zip",
    }

    try:
        if reset:
            if os.path.exists(exe_dir):
                shutil.rmtree(exe_dir)

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
            # Get downloaded zip file extension
            zip_ext = os.path.splitext(zip_name)[1]
            # Download WhiteboxTools
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

                    def is_within_directory(directory, target):
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)

                        prefix = os.path.commonprefix([abs_directory, abs_target])

                        return prefix == abs_directory

                    def safe_extract(
                        tar, path=".", members=None, *, numeric_owner=False
                    ):
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")

                        tar.extractall(path, members, numeric_owner=numeric_owner)

                    safe_extract(tar_ref, pkg_dir)
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
            runner_name = "whitebox_runner{}".format(exe_ext)
            runner_path = os.path.join(exe_dir, runner_name)

            # grant executable permission
            if platform.system() != "Windows":
                os.system("chmod 755 " + exe_path)
                os.system("chmod 755 " + runner_path)
            plugins = list(
                set(glob.glob(os.path.join(new_plugin_dir, "*")))
                - set(glob.glob(os.path.join(new_plugin_dir, "*.json")))
            )
            if platform.system() != "Windows":
                for plugin in plugins:
                    os.system("chmod 755 " + plugin)

            exe_path_new = os.path.join(pkg_dir, exe_name)
            shutil.copy(exe_path, exe_path_new)
            runner_path_new = os.path.join(pkg_dir, runner_name)
            shutil.copy(runner_path, runner_path_new)

            try:
                os.remove(zip_name)
            except:
                pass

            # # The official WhiteboxTools Linux binary from whiteboxgeo.com requires GLIBC 2.29,
            # # which is incompatible with Google Colab that uses GLIBC 2.27. The following code
            # # downloads the binary that is compatible with Google Colab.
            if "google.colab" in sys.modules:
                # url = "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_ubuntu_18.04.zip"
                url = "https://www.whiteboxgeo.com/WBT_Linux/WhiteboxTools_linux_musl.zip"

                zip_name = os.path.join(pkg_dir, os.path.basename(url))
                try:
                    request = urllib.request.urlopen(url, timeout=500)
                    with open(zip_name, "wb") as f:
                        f.write(request.read())
                    os.remove(exe_path)
                    with zipfile.ZipFile(zip_name, "r") as zip_ref:
                        zip_ref.extractall(pkg_dir)
                    os.system("chmod 755 " + exe_path)
                    plugins = list(
                        set(glob.glob(os.path.join(new_plugin_dir, "*")))
                        - set(glob.glob(os.path.join(new_plugin_dir, "*.json")))
                    )
                    for plugin in plugins:
                        os.system("chmod 755 " + plugin)
                except Exception as e:
                    print(e)

            webbrowser.open("https://www.whiteboxgeo.com/", new=2)

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
