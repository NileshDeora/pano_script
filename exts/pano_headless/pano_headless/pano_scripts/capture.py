from typing import Optional
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


# Let's define a model to handle the parsing of incoming requests.
#
# Using `pydantic` to handle data-parsing duties makes it less cumbersome for us to do express types, default values,
# minimum/maximum values, etc. while also taking care of documenting input and output properties of our service using
# the OpenAPI specification format.
class ViewportCaptureRequestModel(BaseModel):
    """Model describing the request to capture a viewport as an image."""

    url: str = Field(
        ...,
        title="Model Url",
        description="url",
    )
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
    other_vw2: str = Field(
    ...,
    title="other_vw2 Url",
    description="url",
    )
    other_vw3: str = Field(
    ...,
    title="other_vw3 Url",
    description="url",
    )
    # If required, add additional capture response options in subsequent iterations.
    # [...]

# We will also define a model to handle the delivery of responses back to clients.
#
# Just like the model used to handle incoming requests, the model to deliver responses will not only help define
# default values of response parameters, but also in documenting the values clients can expect using the OpenAPI
# specification format.
class ViewportCaptureResponseModel(BaseModel):
    """Model describing the response to the request to capture a viewport as an image."""

    success: bool = Field(
        default=False,
        title="Capture status",
        description="Status of the capture of the given USD stage.",
    )
    captured_image_path: Optional[str] = Field(
        default=None,
        title="Captured image path",
        description="Path of the captured image, hosted on the current server.",
    )
    error_message: Optional[str] = Field(
        default=None,
        title="Error message",
        description="Optional error message in case the operation was not successful.",
    )
    # If required, add additional capture response options in subsequent iterations.
    # [...]


# Using the `@router` annotation, we'll tag our `capture` function handler to document the responses and path of the
# API, once again using the OpenAPI specification format.
@router.post(
    path="/make_pano",
    summary="Capture a given USD stage",
    description="Capture a given USD stage as an image.",
    response_model=ViewportCaptureResponseModel,
)
async def make_pano(request: ViewportCaptureRequestModel,) -> ViewportCaptureResponseModel:
    # For now, let's just print incoming request to the log to confirm all components of our extension are properly
    data = {
        "url": request.url,
        "main_vw": request.main_vw,
        "other_vw1": request.other_vw1,
        "other_vw2": request.other_vw2,
        "other_vw3": request.other_vw3,
    }
    # wired together:
    print(data)
    # Example usage:
    try:
        if validate_object(data):
            print("Validation successful.")
            panoData = [{
            "url":request.url,
            "vw_data": [
            {"main_vw": request.main_vw},
            {"other_vw1":request.other_vw1},
            {"other_vw2":request.other_vw2},
            {"other_vw3":request.other_vw3},
            ]
            }
            ]
            print(panoData)
            set_viewport_res()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            file_name = '/output/pano.png'
            print(parent_dir+file_name)
            outPath = parent_dir+file_name
            # capture(outPath).
            stage = omni.usd.get_context().get_stage()
            isUsdLoad = stage.GetPrimAtPath("/Environment/Camera")
            print('isUsdLoad', isUsdLoad)
            if isUsdLoad:
                for data in  panoData:   
                    loadmodel_fun(data)
                    setup_camera_fun()
                    update_vw_fun(data["vw_data"])
                    # def callback(success, captured_image_path):
                    #     print(captured_image_path)
                    capture(outPath)
                    for x in range(3000):
                        await omni.kit.app.get_app().next_update_async()
                    # omni.kit.actions.core.execute_action("omni.kit.menu.edit", "capture_screenshot", callback)
                return ViewportCaptureResponseModel(
                    success=True,
                    captured_image_path= outPath,
                    error_message="Success!",
                )
            else:
                return ViewportCaptureResponseModel(
                    success=False,
                    captured_image_path= None,
                    error_message="Stage is not ready!",
                )
    except ValueError as e:
        # print(f"Validation failed: {e}")
        return ViewportCaptureResponseModel(
            success=False,
            captured_image_path= None,
            error_message= "Validation failed",
        )



    

   