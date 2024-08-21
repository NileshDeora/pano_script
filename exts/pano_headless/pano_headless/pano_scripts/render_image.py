from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file
import asyncio
import omni.kit.commands
from .reset_stage import *
import os
import carb
from .upscale_image import *


async def capture_frame(outdata):
    print("capturing pano, Start...")
    outdata["outPath"] = OutPutPath(outdata)

    omni.kit.commands.execute('SelectPrims',
    old_selected_paths=['/World'],
    new_selected_paths=[],
    expand_in_stage=True)
    opts = carb.settings.get_settings().set("persistent/app/viewport/displayOptions", 0)

    await omni.kit.app.get_app().next_update_async()
    viewport = get_active_viewport()
    def switch(res):
        if res == "1k":
            viewport.resolution = (1920 , 1080)
        if res == "2k":
            viewport.resolution = (2*1920 , 2*1080)
        elif res == "4k":
            viewport.resolution = (4000 , 2250)
        elif res == "5k":
            viewport.resolution = (5120 , 2880)
        elif res == "6k":
            viewport.resolution = (6144 , 3456)
        elif res == "7k":
            viewport.resolution = (7000, 3937)
        elif res == "8k":
            viewport.resolution = (8000, 4500)
        elif res == "9k":
            viewport.resolution = (9000, 5062)            
    switch(outdata["res"])

    await omni.kit.app.get_app().next_update_async()

    def switch(res):
        if res == "1k":
            return [200 , 10]
        if res == "2k":
            return [200 , 10]
        elif res == "4k":
            return [20000 , 500]
        elif res == "5k":
            return [3000 , 500]
        elif res == "6k":
            return [5000 , 500]
        elif res == "7k":
            return [6000 , 500]
        elif res == "8k":
            return [5000 , 500]
        elif res == "9k":
            return [7000 , 1000]
        

    printTime = switch(outdata["res"])

    await printIt(printTime, outdata, viewport)

def capture(outPath):
    asyncio.ensure_future(capture_frame(outPath))


async def printIt(data, outdata,viewport):
        #set range 5k for 7k
    for x in range(data[0]):
        await omni.kit.app.get_app().next_update_async()
    capture = capture_viewport_to_file(viewport, file_path=outdata['outPath'])
    for x in range(data[1]):
        await omni.kit.app.get_app().next_update_async()
    print("capture done", outdata, capture)
    await asyncio.sleep(5)
    resetView()
    resize(outdata['outPath'])
    

def OutPutPath(outdata):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir) + '/'+outdata["folder"]+'/'
    file_name = outdata["name"]
    return parent_dir+file_name+'.png'