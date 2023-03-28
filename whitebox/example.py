#!/usr/bin/env python
'''
This module provides examples for calling tools/functions in WhiteboxTools library
Only works for Python 3.x
Source: https://jblindsay.github.io/ghrg/WhiteboxTools
GitHub: https://github.com/jblindsay/whitebox-tools
'''

import os
import sys
from whitebox_tools import WhiteboxTools


if __name__ == '__main__':
    try:
        wbt = WhiteboxTools()

        root_dir = os.path.dirname(os.path.abspath(__file__))
        # exe_dir = os.path.join(root_dir, "WBT")
        exe_dir = os.path.dirname(os.path.abspath(__file__))

        wbt.set_whitebox_dir(exe_dir)
        wbt.work_dir = os.path.join(root_dir, "testdata")
        wbt.verbose = False

        # Prints the whitebox-tools version
        print("\nVersion information: {}".format(wbt.version()))
        # Prints the whitebox-tools license
        print(wbt.license())
        # Prints the whitebox-tools help...a listing of available commands
        print(wbt.help())
        # List all available tools in whitebox-tools
        # Print the help for a specific tool.
        print(wbt.tool_help("breach_depressions"))

        # print("ALl available tools: {}\n".format(wbt.list_tools()))
        all_tools = wbt.list_tools()
        print("\nAll Available Tools:")
        for index, tool in enumerate(all_tools):
            print(
                "{} {}: {} ...".format(
                    str(index + 1).zfill(3), tool, all_tools[tool][:45]
                )
            )

        # Lists tools with 'lidar' or 'LAS' in tool name or description.
        lidar_tools = wbt.list_tools(['lidar', 'LAS'])
        print("\nAvailable LiDAR Tools:")
        for index, tool in enumerate(lidar_tools):
            print(
                "{} {}: {} ...".format(
                    str(index + 1).zfill(3), tool, all_tools[tool][:45]
                )
            )
        # print("lidar tools: {}\n".format(wbt.list_tools(['lidar', 'LAS'])))

        # Notice that tool names within WhiteboxTools.exe are CamelCase but
        # you can also use snake_case here, e.g. print(wbt.tool_help("breach_depressions"))

        # Call some tools, do some work
        wbt.feature_preserving_smoothing("DEM.tif", "smoothed.tif", filter=9)
        wbt.breach_depressions("smoothed.tif", "breached.tif")
        wbt.d_inf_flow_accumulation("breached.tif", "flow_accum.tif")

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        # For 'permission denied', you need to ensure that whitebox_tools has executable permission
        # cd /path/to/folder/WBT"
        # chmod 755 whitebox_tools"
