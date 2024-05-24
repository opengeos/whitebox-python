===============
whitebox-python
===============

.. image:: https://colab.research.google.com/assets/colab-badge.svg
        :target: https://gishub.org/whitebox-colab

.. image:: https://mybinder.org/badge_logo.svg 
        :target: https://gishub.org/whitebox-cloud

.. image:: https://img.shields.io/pypi/v/whitebox.svg
        :target: https://pypi.python.org/pypi/whitebox

.. image:: https://pepy.tech/badge/whitebox
        :target: https://pepy.tech/project/whitebox

.. image:: https://anaconda.org/conda-forge/whitebox/badges/version.svg
        :target: https://anaconda.org/conda-forge/whitebox

.. image:: https://readthedocs.org/projects/whitebox/badge/?version=latest
        :target: https://whitebox.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/Donate-Buy%20me%20a%20coffee-yellowgreen.svg
        :target: https://www.buymeacoffee.com/opengeos


Important Note
--------------
.. image:: https://i.imgur.com/Ic8BA7C.png

This repository is related to the WhiteboxTools Python Frontend only. You can report issues to this repo if you have problems installing this Python package. If you encounter any tool functioning specific errors, please `open an issue`_ on Dr. John Lindsay's WhiteboxTools_ repo.  

**Links**

* Authors: Dr. John Lindsay (https://jblindsay.github.io/ghrg/index.html)
* Contributors: Dr. Qiusheng Wu (https://wetlands.io)
* GitHub repo: https://github.com/opengeos/whitebox-python
* WhiteboxTools: https://github.com/jblindsay/whitebox-tools
* User Manual: https://www.whiteboxgeo.com/manual/wbt_book/intro.html
* PyPI: https://pypi.org/project/whitebox/
* conda-forge: https://anaconda.org/conda-forge/whitebox
* Documentation: https://whitebox.readthedocs.io
* Binder: https://gishub.org/whitebox-cloud
* Free software: `MIT license`_


**Contents**

- `Description`_
- `Installation`_
- `whitebox Tutorials`_
- `whitebox GUI`_
- `Available Tools`_
- `Supported Data Formats`_
- `Contributing`_
- `License`_
- `Reporting Bugs`_
- `Credits`_



Description
-----------
The **whitebox** Python package is built on **WhiteboxTools**, an advanced geospatial data analysis platform developed by Prof. John Lindsay (webpage_; jblindsay_) at the University of Guelph's `Geomorphometry and Hydrogeomatics Research Group`_. *WhiteboxTools* can be used to perform common geographical information systems (GIS) analysis operations, such as cost-distance analysis, distance buffering, and raster reclassification. Remote sensing and image processing tasks include image enhancement (e.g. panchromatic sharpening, contrast adjustments), image mosaicing, numerous filtering operations, simple classification (k-means), and common image transformations. *WhiteboxTools* also contains advanced tooling for spatial hydrological analysis (e.g. flow-accumulation, watershed delineation, stream network analysis, sink removal), terrain analysis (e.g. common terrain indices such as slope, curvatures, wetness index, hillshading; hypsometric analysis; multi-scale topographic position analysis), and LiDAR data processing. LiDAR point clouds can be interrogated (LidarInfo, LidarHistogram), segmented, tiled and joined, analyized for outliers, interpolated to rasters (DEMs, intensity images), and ground-points can be classified or filtered. *WhiteboxTools* is not a cartographic or spatial data visualization package; instead it is meant to serve as an analytical backend for other data visualization software, mainly GIS.


Installation
------------
**whitebox** supports a variety of platforms, including Microsoft Windows, macOS, and Linux operating systems. Note that you will need to have Python 3.x installed. Python 2.x is not supported. The **whitebox** Python package can be installed using the following command: 

.. code:: python

  pip install whitebox


If you have installed **whitebox** Python package before and want to upgrade to the latest version, you can use the following command:

.. code:: python

  pip install whitebox -U


It is recommended that you use a Python virtual environment (e.g., conda) to test the whitebox package. Please follow the `conda user guide`_ to install conda if necessary. Once you have conda installed, you can use Terminal or an Anaconda Prompt to create a Python virtual environment. Check `managing Python environment`_ for more information.

.. code:: python

  conda create -n wbt python
  source activate wbt
  conda install whitebox -c conda-forge

If you encounter an GLIBC errors when installing the whitebox package, you can try the following command:

.. code:: python

  import whitebox
  whitebox.download_wbt(linux_musl=True, reset=True)


Alternatively, you can set the environment variable ``WBT_LINUX`` to ``MUSL`` before installing the whitebox package. It will automatically download the MUSL version of WhiteboxTools.

.. code:: python

  import os
  os.environ["WBT_LINUX"] = "MUSL"

whitebox Tutorials
------------------

Launch the whitebox tutorial notebook directly with **mybinder.org** now:

.. image:: https://mybinder.org/badge_logo.svg 
        :target: https://gishub.org/whitebox-cloud

Quick Example
=============

Tool names in the **whitebox** Python package can be called either using the snake_case or CamelCase convention (e.g. *lidar_info* or *LidarInfo*). See below for an example Python script (example.py_). If you are interested in using the *WhiteboxTools* command-line program, check `WhiteboxTools Usage`_.

.. code:: python

    import os
    import pkg_resources
    import whitebox

    wbt = whitebox.WhiteboxTools()
    print(wbt.version())
    print(wbt.help())

    # identify the sample data directory of the package
    data_dir = os.path.dirname(pkg_resources.resource_filename("whitebox", 'testdata/'))

    wbt.set_working_dir(data_dir)
    wbt.verbose = False
    wbt.feature_preserving_smoothing("DEM.tif", "smoothed.tif", filter=9)
    wbt.breach_depressions("smoothed.tif", "breached.tif")
    wbt.d_inf_flow_accumulation("breached.tif", "flow_accum.tif")


A Jupyter Notebook Tutorial for whitebox
========================================

This tutorial can be accessed in three ways:

- HTML version: https://gishub.org/whitebox-html
- Viewable Notebook: https://gishub.org/whitebox-notebook
- Interactive Notebook: https://gishub.org/whitebox-cloud

Launch this tutorial as an interactive Jupyter Notebook on the cloud - https://gishub.org/whitebox-cloud.

.. image:: https://i.imgur.com/LF4UE1j.gif


whitebox GUI
------------

WhiteboxTools also provides a Graphical User Interface (GUI) - **WhiteboxTools Runner**, which can be invoked using the following Python script:

.. code:: python

  import whitebox
  whitebox.Runner()

.. image:: https://wetlands.io/file/images/whitebox.png





Troubleshooting
---------------

Linux
=====
When using ``import whitebox``, if you get an error that says ``No module named '_tkinter', please install the python3-tk package``, you can try the following solution:

- For Ubuntu, Linux Mint, etc: ``sudo apt-get install python3-tk``
- For Manjaro, Arch Linux: ``sudo pacman -S tk``




Available Tools
---------------
The library currently contains **518** tools, which are each grouped based on their main function into one of the following categories: Data Tools, GIS Analysis, Hydrological Analysis, Image Analysis, LiDAR Analysis, Mathematical and Statistical Analysis, Stream Network Analysis, and Terrain Analysis. For a listing of available tools, complete with documentation and usage details, please see the `WhiteboxTools User Manual`_.


Supported Data Formats
----------------------

The WhiteboxTools library currently supports read/writing raster data in Whitebox GAT, GeoTIFF, ESRI (ArcGIS) ASCII and binary (.flt & .hdr), GRASS GIS, Idrisi, SAGA GIS (binary and ASCII), and Surfer 7 data formats. At present, there is limited ability in WhiteboxTools to read vector geospatial data. Support for Shapefile (and other common vector formats) will be enhanced within the library soon. 

Contributing
------------

If you would like to contribute to the project as a developer, follow these instructions to get started:

1. Fork the whitebox project (https://github.com/opengeos/whitebox-python)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request

License
-------

The **whitebox** package is distributed under the `MIT license`_, a permissive open-source (free software) license.


Reporting Bugs
--------------
Report bugs at https://github.com/opengeos/whitebox-python/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _example.py: https://github.com/opengeos/whitebox-python/blob/master/whitebox/example.py
.. _WhiteboxTools: https://github.com/jblindsay/whitebox-tools
.. _webpage: https://jblindsay.github.io/ghrg/index.html
.. _jblindsay: https://github.com/jblindsay
.. _`Geomorphometry and Hydrogeomatics Research Group`: https://jblindsay.github.io/ghrg/index.html
.. _`conda user guide`: https://conda.io/docs/user-guide/install/index.html
.. _`managing Python environment`: https://conda.io/docs/user-guide/tasks/manage-environments.html
.. _`WhiteboxTools Usage`: https://github.com/jblindsay/whitebox-tools#3-usage
.. _`MIT license`: https://opensource.org/licenses/MIT
.. _`open an issue`: https://github.com/jblindsay/whitebox-tools/issues
.. _`WhiteboxTools User Manual`: https://www.whiteboxgeo.com/manual/wbt_book/intro.html
