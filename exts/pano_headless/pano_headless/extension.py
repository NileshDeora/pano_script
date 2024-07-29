import omni.ext
import asyncio
from .pano_scripts.load_usd import *
# from .pano_scripts.load_model import *
# from .pano_scripts.setup_camera import *
# from .pano_scripts.update_vw import *
# from .pano_scripts.set_viewport_res import *
# from .pano_scripts.render_image import *
# from .parallax_scripts.shopping_area.grid import *
# from .parallax_scripts.shopping_area.capture_walls import *
from .pano_scripts.upscale_image import *
from omni.services.core import main
import omni.usd
from .routes.routes import *
import carb
http_server_port = carb.settings.get_settings().get_as_int("exts/omni.services.transport.server.http/port")
print(f"The OpenAPI specifications can be accessed at: http://localhost:{http_server_port}/docs")
# import omni.kit.pipapi
# omni.kit.pipapi.install("sched")

# Example: Iterating over a list
panoData = [{
     "url":"https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/vtour/dollhouse_59_2024_04_10_06_59_44/model.glb",
     "vw_data": [
     {"main_vw":"https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6785_2_1714486077637.png"},
     {"other_vw1":"https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6786_2_1714486788541.png"},
     {"other_vw2":"https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6787_2_1714639976079.png"},
     {"other_vw3":"https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6788_2_1714487401706.png"},
     ]
     }
     ]

def list_meshes():
    return "pong"   

# asyncio.ensure_future(open_usd_project())


class PanoExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        # print("pano startup", omni.kit.window.content_browser)
        initRoutes(self, ext_id)
        # upscale()
        # capture_walls_await() 
        # ext_name = ext_id.split("-")[0]
        # url_prefix = carb.settings.get_settings().get_as_string(f"exts/{ext_name}/url_prefix")
        # print(url_prefix,ext_name)
        # main.register_router(router=router, prefix='', tags=["Viewport capture"],)
        # list_meshes()
        # main.register_endpoint("get", "/list_meshes", list_meshes, tags=["Simple Service"])
        # set_viewport_res()
        # for data in  panoData:   
        #     loadmodel_fun(data)
        #     setup_camera_fun()
        #     update_vw_fun(data["vw_data"])
            # capture()

    def on_shutdown(self):
        print("pano shutdown")
        main.deregister_endpoint("get", "/list_meshes")
        
