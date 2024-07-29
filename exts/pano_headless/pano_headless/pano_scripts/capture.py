from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from ..pano_scripts.load_usd import *
from ..pano_scripts.load_model import *
from ..pano_scripts.setup_camera import *
from ..pano_scripts.update_vw import *
from ..pano_scripts.set_viewport_res import *
from ..pano_scripts.render_image import *
from ..pano_scripts.validation import *
# import carb

from omni.services.core import routers


router = routers.ServiceAPIRouter()


class ViewportCaptureRequestModel(BaseModel):
    main_vw: str = Field(
        ...,
        title="main_vw Url",
        description="url",
    )
    other_vw1: str = Field(
    ...,
    title="other_vw1 Url",
    description="url",
    )
    shop_id: str = Field(
    ...,
    title="shop id",
    description="id",
    )
  
  
    # If required, add additional capture response options in subsequent iterations.
    # [...]

class ViewportCaptureResponseModel(BaseModel):
    """Model describing the response to the request to capture a viewport as an image."""

    success: bool = Field(
        default=False,
        title="Capture status",
        description="Status of the capture of the given USD stage.",
    )
    # captured_image_path: Optional[str] = Field(
    #     default=None,
    #     title="Captured image path",
    #     description="Path of the captured image, hosted on the current server.",
    # )
    # error_message: Optional[str] = Field(
    #     default=None,
    #     title="Error message",
    #     description="Optional error message in case the operation was not successful.",
    # )
    # If required, add additional capture response options in subsequent iterations.
    # [...]

class NestedViewportCaptureRequestModel(BaseModel):
    __root__: Dict[str, List[ViewportCaptureRequestModel]]

# Using the `@router` annotation, we'll tag our `capture` function handler to document the responses and path of the
# API, once again using the OpenAPI specification format.
@router.post(
    path="/make_pano",
    summary="Capture a given USD stage",
    description="Capture a given USD stage as an image.",
    response_model=ViewportCaptureResponseModel,
)

async def make_pano(request: NestedViewportCaptureRequestModel,) -> ViewportCaptureResponseModel:
    root_dict = request.__root__
    for sa_id, sa_data in root_dict.items():
        print('key', sa_id)
        if sa_id in root_dict:
            if len(root_dict[sa_id]) > 0:
                for shop in root_dict[sa_id]:
                    print('shop data',shop)
                    await applyVW(shop, sa_id)
        else:
            print(f"Key '{sa_id}' not found in the request")
        
        for x in range(100):
            await omni.kit.app.get_app().next_update_async()
        
    renderData = {
                        "res" : '7k',
                        "name": "7k",
                        "folder": "upscale_model/upscale/media",
                        "reset_view": True,
                    }
    # capture(renderData)

    return ViewportCaptureResponseModel(
                    success=True,
                )

    
async def applyVW(request, sa_id):
    data = {
        "main_vw": request.main_vw,
        "other_vw1": request.other_vw1,
    }
    print("applyvWWWW")
    try:
        if validate_object(data):
            print("Validation successful.")
            
            panoData = [{
            "vw_data": [
            { "sa"+sa_id+"_s"+ request.shop_id +"_"+"main_vw": request.main_vw},
            {"sa"+sa_id+"_s"+ request.shop_id +"_"+"other_vw1":request.other_vw1},
            ]
            }
            ]
            # set_viewport_res()
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # parent_dir = os.path.dirname(current_dir) + '/output/'
            # file_name = 'pano.png'
            # print(parent_dir+file_name)
            # outPath = parent_dir+file_name
            # capture(outPath).
            stage = omni.usd.get_context().get_stage()
            isUsdLoad = stage.GetPrimAtPath("/Environment/Camera")
            # print('isUsdLoad', isUsdLoad)
            if isUsdLoad:
                for data in  panoData:   
                    # loadmodel_fun(data)
                    # setup_camera_fun()
                    update_vw_fun(data["vw_data"], sa_id)
                    for x in range(10):
                        await omni.kit.app.get_app().next_update_async()
                    # def callback(success, captured_image_path):
                    #     print(captured_image_path)
                    
                    # for x in range(3000):
                    #     await omni.kit.app.get_app().next_update_async()
                    # omni.kit.actions.core.execute_action("omni.kit.menu.edit", "capture_screenshot", callback)
            else:
                return ViewportCaptureResponseModel(
                    success=False
                )
    except ValueError as e:
        # print(f"Validation failed: {e}")
        return ViewportCaptureResponseModel(
            success=False
        )


   