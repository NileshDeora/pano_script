import omni.kit.commands
import omni
from pxr import UsdGeom
from omni.kit.viewport.utility import get_active_viewport
from pxr import Gf, Usd, Sdf
import asyncio

async def setup_camera(sa_id):
    for x in range(5):
        await omni.kit.app.get_app().next_update_async()
    camera_path = "/Environment/cam_parcel_" + sa_id
    print("Setting up camera", camera_path)
    viewport = get_active_viewport()
    viewport.camera_path = camera_path
    


def setup_camera_fun(sa_id):
    asyncio.ensure_future(setup_camera(sa_id))