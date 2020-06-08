##################################################################
# Steps for updating the whitebox Python package
# Step 1 - Delete the existing develop branch: git branch -D develop  
# Step 2 - Create a new develop branch: git checkout -b develop
# Step 3 - Delete the old WhiteboxTools_linux_amd64.tar.xz if needed
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
import tarfile
import urllib.request

linux_tar = "WhiteboxTools_linux_amd64.tar.xz"
work_dir = os.path.dirname(__file__)
tar_path = os.path.join(work_dir, linux_tar)
WBT_dir = os.path.join(work_dir, "WBT")
old_img_dir = os.path.join(WBT_dir, "img")
new_img_dir = os.path.join(work_dir, "img")

if not os.path.exists(tar_path):
    print("Downloading WhiteboxTools binary ...")
    url = "https://jblindsay.github.io/ghrg/WhiteboxTools/WhiteboxTools_linux_amd64.tar.xz"
    urllib.request.urlretrieve(url, tar_path)   # Download WhiteboxTools
else:
    print("WhiteboxTools binary already exists.")

if os.path.exists(WBT_dir):
    shutil.rmtree(WBT_dir)

print("Decompressing {} ...".format(linux_tar))
with tarfile.open(tar_path, "r") as tar_ref:
    tar_ref.extractall(work_dir)

if os.path.exists(new_img_dir):
    shutil.rmtree(new_img_dir)

shutil.copytree(old_img_dir, new_img_dir)

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
        f.write(line)
        if line.strip() == "from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW":
            with open(os.path.join(work_dir, "download_wbt.py")) as f_dl:
                dl_lines = f_dl.readlines()
                f.writelines(dl_lines[1:])
        elif line.strip() == "self.default_callback = default_callback":
            f.write("        download_wbt()\n")

shutil.move(os.path.join(WBT_dir, 'whitebox_tools'), os.path.join(work_dir, 'whitebox_tools'))


f.close()

        
