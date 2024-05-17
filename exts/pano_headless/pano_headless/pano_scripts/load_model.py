import omni.kit.commands
from pxr import Sdf
import asyncio



async def load_model(data):
    stage = omni.usd.get_context().get_stage()
    context: omni.usd.UsdContext = omni.usd.get_context()
    omni.kit.commands.execute('CreatePayloadCommand',
	usd_context=omni.usd.get_context(),
	path_to=Sdf.Path('/Environment/shop'),  
	asset_path= data['url'],
    instanceable=True
	)
    




def loadmodel_fun(data):
    asyncio.ensure_future(load_model(data))