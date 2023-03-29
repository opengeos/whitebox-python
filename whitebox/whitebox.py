# -*- coding: utf-8 -*-

"""Main module."""

from .whitebox_tools import download_wbt, WhiteboxTools

def Runner(clear_app_state=False, callback=None):
    wbt = WhiteboxTools()
    wbt.launch_wb_runner(clear_app_state, callback)