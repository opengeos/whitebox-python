=====
Usage
=====

To use whitebox in a project::

    import whitebox

For example:

.. code:: python

    import os
    from importlib_resources import files
    import whitebox

    wbt = whitebox.WhiteboxTools()
    print(wbt.version())
    print(wbt.help())

    # identify the sample data directory of the package
    data_dir = str(files("whitebox").joinpath("testdata"))

    wbt.set_working_dir(data_dir)
    wbt.verbose = False
    wbt.feature_preserving_denoise("DEM.tif", "smoothed.tif", filter=9)
    wbt.breach_depressions("smoothed.tif", "breached.tif")
    wbt.d_inf_flow_accumulation("breached.tif", "flow_accum.tif")

Check the example.py_ for more details.

.. _example.py: https://github.com/opengeos/whitebox-python/blob/master/whitebox/example.py