from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file
import asyncio
import omni.kit.commands
from .reset_stage import *



async def capture_frame(outPath):
    await omni.kit.app.get_app().next_update_async()
    viewport = get_active_viewport()
    # viewport.resolution = (5120 , 2880)
    viewport.resolution = (1920 , 1080)
    # viewport.resolution = (7000, 3937)
    await omni.kit.app.get_app().next_update_async()
    #set range 5k for 7k
    for x in range(3000):
        await omni.kit.app.get_app().next_update_async()
    capture = capture_viewport_to_file(viewport, file_path=outPath)
    print("capture done")
    for x in range(2000):
        await omni.kit.app.get_app().next_update_async()
    resetView()

def capture(outPath):
    asyncio.ensure_future(capture_frame(outPath))