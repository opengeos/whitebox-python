##################################################################
# Steps for updating the whitebox Python package
# Step 1 - Delete the existing develop branch: git branch -D develop
# Step 2 - Create a new develop branch: git checkout -b develop
# Step 3 - Delete the old WhiteboxTools_linux_amd64.zip if needed
# Step 4 - Run automation.py
# Step 5 - Create a conda environment: conda create -n wbt python
# Step 6 - Install dependencies: pip install -r requirements_dev.txt
# Step 7 - Install whitebox: pip install -e .
# Step 8 - Run example.py
# Step 9 - Commit and push changes
# Step 10 - Merge pull request on GitHub
# Step 11 - Switch to master branch and pull updates: git checkout master | git pull
# Step 12 - Update version number: bumpversion patch/minor/major | git push --tags | git push
# Step 13 - Create package: python setup.py sdist
# Step 14 - Upload package to PyPI: twine upload dist/whitebox-*.*.*.tar.gz
##################################################################

import os
import shutil
import zipfile
import urllib.request

linux_zip = "WhiteboxTools_linux_amd64.zip"
work_dir = os.path.dirname(__file__)
zip_path = os.path.join(work_dir, linux_zip)
WBT_dir = os.path.join(work_dir, "WBT")
init_img_dir = os.path.join(WBT_dir, "img")
new_img_dir = os.path.join(work_dir, "img")
init_plugin_dir = os.path.join(WBT_dir, "plugins")
new_plugin_dir = os.path.join(work_dir, "plugins")

if not os.path.exists(zip_path):
    print("Downloading WhiteboxTools binary ...")
    # url = "https://github.com/giswqs/whitebox-bin/raw/master/WhiteboxTools_linux_amd64.zip"
    url = "https://www.whiteboxgeo.com/WBT_Linux/WhiteboxTools_linux_amd64.zip"
    urllib.request.urlretrieve(url, zip_path)  # Download WhiteboxTools
else:
    print("WhiteboxTools binary already exists.")

if os.path.exists(WBT_dir):
    shutil.rmtree(WBT_dir)

print("Decompressing {} ...".format(linux_zip))
with zipfile.ZipFile(zip_path, "r") as tar_ref:
    tar_ref.extractall(work_dir)

if os.path.exists(new_img_dir):
    shutil.rmtree(new_img_dir)

if os.path.exists(new_plugin_dir):
    shutil.rmtree(new_plugin_dir)

shutil.copytree(init_img_dir, new_img_dir)
shutil.copytree(init_plugin_dir, new_plugin_dir)

print("Generating wb_runner.py ...")
with open(os.path.join(WBT_dir, "wb_runner.py")) as f_runner:
    lines = f_runner.readlines()
    for index, line in enumerate(lines):
        if line.strip() == "from whitebox_tools import WhiteboxTools, to_camelcase":
            line = "from .whitebox_tools import WhiteboxTools, to_camelcase\n"
            lines[index] = line
            # print("{}: {}".format(index, line))
        elif line.strip() == "def main():":
            line = "def Runner():\n"
            lines[index] = line
            # print("{}: {}".format(index, line))
        elif line.strip() == "main()":
            line = "    Runner()\n"
            lines[index] = line
            # print("{}: {}".format(index, line))

    runner_path = os.path.join(work_dir, "wb_runner.py")
    if os.path.exists(runner_path):
        os.remove(runner_path)

    with open(runner_path, "w") as f_runner_w:
        f_runner_w.writelines(lines)


wbt_path = os.path.join(work_dir, "whitebox_tools.py")
if os.path.exists(wbt_path):
    os.remove(wbt_path)

f = open(wbt_path, "w")

print("Generating whitebox_tools.py ...")
with open(os.path.join(WBT_dir, "whitebox_tools.py")) as f_wbt:
    lines = f_wbt.readlines()
    for index, line in enumerate(lines):
        if line.strip() == "os.chdir(self.exe_path)":
            f.write("            work_dir = os.getcwd()\n")
        f.write(line)

        if line.strip() == "from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW":
            with open(os.path.join(work_dir, "download_wbt.py")) as f_dl:
                dl_lines = f_dl.readlines()
                f.write("\n")
                f.writelines(dl_lines)
        elif line.strip() == "self.__max_procs = -1":
            f.write("        download_wbt()\n")

        if line.strip() in ["return 1", "return err"]:
            f.write("        finally:\n")
            f.write("            os.chdir(work_dir)\n")


shutil.move(
    os.path.join(WBT_dir, "whitebox_tools"), os.path.join(work_dir, "whitebox_tools")
)


f.close()
