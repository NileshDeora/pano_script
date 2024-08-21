import omni.kit.commands
import omni
from pxr import UsdGeom
# from omni.kit.viewport.utility import get_active_viewport
from pxr import Gf, Usd, Sdf
import asyncio

async def setup_camera():
    for x in range(5):
        await omni.kit.app.get_app().next_update_async()
    print("modelLoad")
    stage = omni.usd.get_context().get_stage()
    cube_prim = stage.GetPrimAtPath("/Environment/shop/camera_1")
    # xformable = UsdGeom.Xformable(cube_prim)
    # matrix = xformable.GetLocalTransformation()
    # translation = matrix.ExtractTranslation()
    target_layer = stage.GetRootLayer()
    # print(translation)

    omni.kit.commands.execute('MovePrim',
	path_from='/Environment/Camera',
	path_to='/Environment/shop/camera_1/Camera',
	keep_world_transform=True,
	destructive=False)


    omni.kit.commands.execute('ChangeProperty',
	prop_path=Sdf.Path('/Environment/shop/camera_1/Camera.xformOp:translate'),
	value=Gf.Vec3d(0.0, 0.0, 0.0),
	prev=Gf.Vec3d(0.0, 0.0, 0.0),
	target_layer=target_layer,
	usd_context_name=Usd.Stage.Open(rootLayer=target_layer, sessionLayer=stage.GetSessionLayer(), pathResolverContext=None))

    omni.kit.commands.execute('ChangeProperty',
	prop_path=Sdf.Path('/Environment/shop/camera_1/Camera.xformOp:rotateYXZ'),
	value=Gf.Vec3d(0.0, 0.0, 0.0),
	prev=Gf.Vec3d(0.0, 0.0, -2.9064642806486916),
	target_layer=target_layer,
	usd_context_name=Usd.Stage.Open(rootLayer=target_layer, sessionLayer=stage.GetSessionLayer(), pathResolverContext=None))


    omni.kit.commands.execute('SelectPrimsCommand',
	old_selected_paths=['/Environment/shop'],
	new_selected_paths=[],
	expand_in_stage=True)


def setup_camera_fun():
    asyncio.ensure_future(setup_camera())