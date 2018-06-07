========
whitebox
========


.. image:: https://img.shields.io/pypi/v/whitebox.svg
        :target: https://pypi.python.org/pypi/whitebox

.. image:: https://img.shields.io/travis/giswqs/whitebox.svg
        :target: https://travis-ci.org/giswqs/whitebox

.. image:: https://readthedocs.org/projects/whitebox/badge/?version=latest
        :target: https://whitebox.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT



An advanced geospatial data analysis platform


* Authors: Dr. John Lindsay (http://www.uoguelph.ca/~hydrogeo/index.html)
* GitHub repos: https://github.com/jblindsay/whitebox-tools | https://github.com/giswqs/whitebox
* PyPI: https://pypi.org/project/whitebox/
* Documentation: https://whitebox.readthedocs.io.
* Free software: MIT license


Features
--------

* TODO


Using It
--------
Install the Python package using the following command:

.. code:: python

  pip install whitebox


And use:

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
    wbt.feature_preserving_denoise("DEM.tif", "smoothed.tif", filter=9)
    wbt.breach_depressions("smoothed.tif", "breached.tif")
    wbt.d_inf_flow_accumulation("breached.tif", "flow_accum.tif")

Check the example.py_ for more details.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _example.py: https://github.com/giswqs/whitebox/blob/master/whitebox/example.py
