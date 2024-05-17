import omni.kit.commands
import asyncio
from pxr import Sdf, Usd
isMainMat = False
firstMat = ""
from .render_image import *

async def update_vw(data):
 print("model loaded")
 for x in range(10):
    await omni.kit.app.get_app().next_update_async()
 print("model loaded")
 global isMainMat
 global firstMat
 for vw in data:
		for key in vw.keys():
			#get child mesh of vw
			def createTexture(vw):
				global isMainMat
				global firstMat

				if isMainMat:
						omni.kit.commands.execute('CopyPrim',
					path_from='/World/Looks/'+firstMat,
					path_to='/World/Looks/'+key,
					exclusive_select=False,
					copy_to_introducing_layer=False)
				else:
					omni.kit.commands.execute('CreateAndBindMdlMaterialFromLibrary',mdl_name='https://omniverse-content-production.s3.us-west-2.amazonaws.com/Materials/2023_2_1/Base/Wood/Plywood.mdl',mtl_name='Plywood',prim_name=key,mtl_created_list=None,bind_selected_prims=True)
					selection = omni.usd.get_context().get_selection()
					selection.set_selected_prim_paths(["/World/Looks/"+key+"/Shader"], False)
					# isMainMat = True
					firstMat = key

			await omni.kit.app.get_app().next_update_async()
			createTexture(vw)
			await omni.kit.app.get_app().next_update_async()

			# asyncio.ensure_future(createTexture(vw))
			async def updateTexture(textvw, textkey):
					await omni.kit.app.get_app().next_update_async()
					print(textvw, textkey)
					stage = omni.usd.get_context().get_stage()
					target_layer = stage.GetRootLayer()
					cube_prim = stage.GetPrimAtPath("/Environment/shop/"+textkey)
					child = cube_prim.GetChildren()
					childMesh = child[0].GetName()
					#Update texture of vw
					omni.kit.commands.execute('ChangeProperty',
					prop_path=Sdf.Path('/World/Looks/'+textkey+'/Shader.inputs:diffuse_texture'),
					value=textvw[textkey],
					prev=None,
					target_layer=target_layer,
					usd_context_name=Usd.Stage.Open(rootLayer=target_layer, sessionLayer=stage.GetSessionLayer(), pathResolverContext=None))
					# Apply default material
					omni.kit.commands.execute('BindMaterialCommand',
					prim_path='/Environment/shop/'+textkey+'/'+childMesh,	
					material_path='/World/Looks/'+textkey,
					)


			await omni.kit.app.get_app().next_update_async()
			asyncio.ensure_future(updateTexture(vw, key))	
			await omni.kit.app.get_app().next_update_async()



def update_vw_fun(data):
    asyncio.ensure_future(update_vw(data))
	
