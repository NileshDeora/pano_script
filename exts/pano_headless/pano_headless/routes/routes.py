from omni import usd 
from pxr import UsdGeom, Usd, Sdf
from omni.services.core import main
from ..pano_scripts.capture import router
import carb
from ..pano_scripts.load_usd import *

def initRoutes(self, ext_id):
    ext_name = ext_id.split("-")[0]
    url_prefix = carb.settings.get_settings().get_as_string(f"exts/{ext_name}/url_prefix")
    print("routes", url_prefix)
    main.register_router(router=router, prefix=url_prefix, tags=["Viewport Pano capture"],)
    main.register_endpoint("get", "/load_usd", load_usd, tags=["Load usd"])
    # main.register_endpoint(router=router, prefix=url_prefix, tags=["Viewport Parallax capture"],)


