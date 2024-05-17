import omni.kit.commands
from .set_viewport_res import *
def resetView():
    set_viewport_res()
	# reset Cam
    omni.kit.commands.execute('MovePrim',
	path_from='/Environment/shop/camera_1/Camera',
	path_to='/Environment/Camera',
	keep_world_transform=True,
	destructive=False)
	
	#delete model
    omni.kit.commands.execute('DeletePrims',
	paths=['/Environment/shop'],
	destructive=False)
	
    omni.kit.commands.execute('DeletePrims',
	paths=['/World/Looks'],
	destructive=False)
    

    