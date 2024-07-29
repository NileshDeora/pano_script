# Async version
import asyncio
import carb
import omni.usd
from .set_viewport_res import *
import os
async def open_usd_project():
	# Synchronous version
	# import omni.usd
	# omni.usd.get_context().open_stage("https://wikipoint.s3.eu-west-1.amazonaws.com/development/file/pano_service.usd", load_set=omni.usd.UsdContextInitialLoadSet.LOAD_NONE)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_name = '/stages/lateral_hall_stage/lateral_hall.usd'
    # file_name = '/stages/pano_service.usd'
    print(parent_dir+file_name)

	#async version
	# result, error = await omni.usd.get_context().open_stage_async("http://omniverse-content-production.s3-us-west-2.amazonaws.com/Samples/Astronaut/Astronaut.usd",load_set=omni.usd.UsdContextInitialLoadSet.LOAD_ALL)
    result, error = await omni.usd.get_context().open_stage_async(parent_dir+file_name,load_set=omni.usd.UsdContextInitialLoadSet.LOAD_ALL)
    stage = omni.usd.get_context().get_stage()
    set_viewport_res()
    print(f"Opened stage {stage} with result {result}")

	# print("usd opened")
	# asyncio.ensure_future(open_usd_project())


async def load_usd():
    asyncio.ensure_future(open_usd_project())
    return "Stage loaded."