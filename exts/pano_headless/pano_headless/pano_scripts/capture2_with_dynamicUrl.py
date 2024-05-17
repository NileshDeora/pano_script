from pydantic import BaseModel, Field
# from ..pano_scripts.load_usd import *
from ..pano_scripts.load_model import *
from ..pano_scripts.setup_camera import *
# from ..pano_scripts.update_vw import *
# from ..pano_scripts.set_viewport_res import *
# from ..pano_scripts.capture import *
# import carb
import asyncio
import os
import shutil
from typing import Optional, Tuple

import carb.settings
import carb.tokens

import omni.kit.actions.core
import omni.kit.app
import omni.usd
from omni.services.core import routers
from omni.kit.viewport.utility import get_active_viewport

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
    usd_stage_path: str = Field(
        ...,
        title="Path of the USD stage for which to capture an image",
        description="Location where the USD stage to capture can be found.",
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
    # wired together:
    # print(f"Received a request to capture an image of \"{request}\".")

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
    # print(panoData)
    # set_viewport_res()
    # outPath = r"C:\Users\NEIL\Downloads\Omni learning\usdcomp-2023.2.5\pano\exts\pano\pano\output\out7k2.png"
    # for data in  panoData:   
    #     loadmodel_fun(data)
    #     setup_camera_fun()
        # update_vw_fun(data["vw_data"])
        # capture(outPath)

    # request.usd_stage_path
    success, captured_image_path, error_message = await capture_viewport(usd_stage_path = request.usd_stage_path)
    return ViewportCaptureResponseModel(
        success=success,
        captured_image_path=captured_image_path,
        error_message=error_message
    )


# Let's include a small utility method to facilitate obtaining the name of the extension our code is bundled with.
# While we could certainly store and share the `ext_id` provided to the `on_startup()` method of our Extension, this
# alternative method of obtaining the name of our extension can also make our code more portable across projects, as it
# may allow you to keep your code changes located closer together and not have to spread them up to the main entrypoint
# of your extension.
def get_extension_name() -> str:
    """
    Return the name of the Extension where the module is defined.

    Args:
        None

    Returns:
        str: The name of the Extension where the module is defined.

    """
    extension_manager = omni.kit.app.get_app().get_extension_manager()
    extension_id = extension_manager.get_extension_id_by_module(__name__)
    extension_name = extension_id.split("-")[0]
    return extension_name


# Building on the utility method just above, this helper method helps us retrieve the path where captured images are
# served from the web server, so they can be presented to clients over the network.
def get_captured_image_path() -> str:
    """
    Return the path where the captured images can be retrieved from the server, in the `/{url_prefix}/{capture_path}`
    format.

    Args:
        None

    Returns:
        str: The path where the captured images can be retrieved from the server.

    """
    extension_name = get_extension_name()
    settings = carb.settings.get_settings()
    url_prefix = settings.get_as_string(f"exts/{extension_name}/url_prefix")
    capture_path = settings.get_as_string(f"exts/{extension_name}/capture_path")

    captured_images_path = f"{url_prefix}{capture_path}"
    return captured_images_path


# In a similar fashion to the utility method above, this helper method helps us retrieve the path on disk where the
# captured images are stored on the server. This makes it possible to map this storage location known to the server to a
# publicly-accessible location on the server, from which clients will be able to fetch the captured images once their
# web-friendly names have been communicated to clients through our Service's response.
def get_captured_image_directory() -> str:
    """
    Return the location on disk where the captured images will be stored, and from which they will be served by the web
    server after being mounted. In order to avoid growing the size of this static folder indefinitely, images will be
    stored under the `${temp}` folder of the Omniverse application folder, which is emptied when the application is shut
    down.

    Args:
        None

    Returns:
        str: The location on disk where the captured images will be stored.

    """
    extension_name = get_extension_name()
    capture_directory_name = carb.settings.get_settings().get_as_string(f"exts/{extension_name}/capture_directory")
    temp_kit_directory = carb.tokens.get_tokens_interface().resolve("${temp}")
    captured_stage_images_directory = os.path.join(temp_kit_directory, capture_directory_name)
    captured_stage_images_directory = os.path.normpath(captured_stage_images_directory)

    return captured_stage_images_directory


# This is the main utility method of our collection so far. This small helper builds on the existing capability of the
# "Edit > Capture Screenshot" feature already available in the menu to capture an image from the Omniverse application
# currently running. Upon completion, the captured image is moved to the storage location that is mapped to a
# web-accessible path so that clients are able to retrieve the screenshot once they are informed of the image's unique
# name when our Service issues its response.
async def capture_viewport(usd_stage_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Capture the viewport, by executing the action already registered in the "Edit > Capture Screenshot" menu.

    Args:
        usd_stage_path (str): Path of the USD stage to open in the application's viewport.

    Returns:
        Tuple[bool, Optional[str], Optional[str]]: A tuple containing a flag indicating the success of the operation,
            the path of the captured image on the web server, along with an optional error message in case of error.

    """
    # success: bool = omni.usd.get_context().open_stage(usd_stage_path)
    success, error = await omni.usd.get_context().open_stage_async(usd_stage_path, load_set=omni.usd.UsdContextInitialLoadSet.LOAD_ALL)
    stage = omni.usd.get_context().get_stage()

    captured_image_path: Optional[str] = None
    error_message: Optional[str] = None

    for x in range(300):
        await omni.kit.app.get_app().next_update_async()

    viewport = get_active_viewport()
    print("usd open?", success, stage, viewport)
    if success:
        event = asyncio.Event()

        menu_action_success: bool = False
        capture_screenshot_filepath: Optional[str] = None
        def callback(success, captured_image_path):
            print('captured_image_path',captured_image_path)
            nonlocal menu_action_success, capture_screenshot_filepath
            menu_action_success = success
            capture_screenshot_filepath = captured_image_path

            event.set()

        omni.kit.actions.core.execute_action("omni.kit.menu.edit", "capture_screenshot", callback)
        await event.wait()
        await asyncio.sleep(delay=1)
        for x in range(300):
            await omni.kit.app.get_app().next_update_async()
        if menu_action_success:
            # Move the screenshot to the location from where it can be served over the network:
            destination_filename = os.path.basename(capture_screenshot_filepath)
            print('destination_filename',destination_filename, capture_screenshot_filepath, get_captured_image_directory())
            destination_filepath = os.path.join(get_captured_image_directory(), destination_filename)
            destination_filepath = os.path.normpath(destination_filepath)
            
            captured_image_path = capture_screenshot_filepath

            # shutil.move(src=capture_screenshot_filepath, dst=destination_filepath)
            # Record the final location of the captured image, along with the status of the operation:
            # captured_image_path = os.path.join(get_captured_image_path(), destination_filename)
            # captured_image_path = os.path.normpath(captured_image_path)

            success = menu_action_success
    else:
        error_message = f"Unable to open stage \"{usd_stage_path}\"."
    print('resultttttt', success, captured_image_path, error_message)
    return (success, captured_image_path, error_message)