import omni.kit.commands
from .set_viewport_res import *
def resetView():
    set_viewport_res()
	
    omni.kit.commands.execute('DeletePrims',
	paths=['/World/Looks'],
	destructive=False)
    print("Reset stage done...")
    

    