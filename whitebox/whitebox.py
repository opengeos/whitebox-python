# -*- coding: utf-8 -*-

"""Main module."""

from .whitebox_tools import download_wbt

def Runner(clear_app_state=False, callback=None):
    from .whitebox_tools import WhiteboxTools
    wbt = WhiteboxTools()
    wbt.launch_wb_runner(clear_app_state, callback)