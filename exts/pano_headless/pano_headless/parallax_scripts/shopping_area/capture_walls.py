from ...pano_scripts.load_model import *
import omni.kit.commands
from omni.kit.viewport.utility import get_active_viewport
from pxr import Gf, Usd, Sdf
from ...pano_scripts.render_image import *
from PIL import Image
from ...parallax_scripts.shopping_area.grid import *

from pxr import Usd
async def capture_walls():
    data = {
        # "url": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/vtour/dollhouse_99_2024_05_17_13_57_25/model.glb"
        # "url" : "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/vtour/dollhouse_50_2024_05_17_16_02_57/model.glb"
        # shopping center
        "url" : "C:/Users/NEIL/Downloads//Retail_Playground_for_parallax_Master-v2/Retail_Playground_for_parallax_Master.gltf"
        
    }
    
    walls = [{'wall_name':'left', 'camera': 'camera_left', "crop_percent":17}, {'wall_name':'right', 'camera': 'camera_right', "crop_percent":17}, {'wall_name':'back', 'camera': 'camera_back', "crop_percent":17}, {'wall_name':'floor', 'camera': 'camera_floor', "crop_percent":0}, {'wall_name':'ceiling', 'camera': 'camera_ceiling', "crop_percent":0}]
    # print("capture walls")
    loadmodel_fun(data)
    for x in range(100):
        await omni.kit.app.get_app().next_update_async()
    hide_walls(walls)
    for x in range(100):  
        await omni.kit.app.get_app().next_update_async()
    for wall in walls:
        await capture_wall(wall) 

def hide_walls(walls):
    for wall in walls:
        omni.kit.commands.execute('ToggleVisibilitySelectedPrims',
        selected_paths=['/Environment/shop/'+wall["wall_name"]],
        stage= omni.usd.get_context().get_stage())



async def capture_wall(wall):
    stage= omni.usd.get_context().get_stage()
    omni.kit.commands.execute('ToggleVisibilitySelectedPrims',
    selected_paths=['/Environment/shop/'+wall["wall_name"]],
    stage= stage)

    target_layer = stage.GetRootLayer()
    path = "/Environment/shop/"+wall["wall_name"]+"/"+wall["camera"]
    mesh = stage.GetPrimAtPath(path)
    mesh_child = mesh.GetChildren()
    cam = mesh_child[0].GetName()
    # print(mesh,mesh_child,cam)

    camera_path = path + "/"+ cam
    # print('cam_path',  camera_path)

    viewport = get_active_viewport()
    # print(viewport, viewport.camera_path)
    viewport.camera_path = camera_path
    omni.kit.commands.execute('ChangeProperty', 
	prop_path=Sdf.Path(camera_path +'.clippingRange'),
	value=Gf.Vec2f(0.10000000149011612, 1000000.0),
	prev=Gf.Vec2f(0.10000000149011612, 1000.0),
    target_layer=target_layer,
	usd_context_name=Usd.Stage.Open(rootLayer=target_layer, sessionLayer=stage.GetSessionLayer(), pathResolverContext=None))
    renderData = {
        "res" : '2k',
        "name": wall["wall_name"],
        "folder": "parallax_output",
        "reset_view": False
    }
    capture(renderData)
    for x in range(400):
        await omni.kit.app.get_app().next_update_async()
    print(wall["wall_name"],'is done')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    parent_dir = os.path.dirname(parent_dir)+'\parallax_output\\'

    img = Image.open(parent_dir+wall["wall_name"]+'.png')
    def crop_image(img, val):
        width, height = img.size
        topval = (val / 100)
        bottomval = (1 - topval)
        print("cropppp",val, topval, bottomval)
        top = height * topval
        bottom = height * bottomval
        return img.crop((0, top, width, bottom))
    cropped = crop_image(img, wall["crop_percent"])
    cropped.save(parent_dir+wall["wall_name"]+'.png')

    omni.kit.commands.execute('ToggleVisibilitySelectedPrims',
    selected_paths=['/Environment/shop/'+wall["wall_name"]],
    stage= stage)

    if wall["wall_name"] == 'ceiling':
        make_grid()

def capture_walls_await():
    asyncio.ensure_future(capture_walls())