from omni.kit.viewport.utility import get_active_viewport


def set_viewport_res():
    viewport = get_active_viewport()
    # print('viewport', viewport)
    # print('viewportsss', viewport)
    viewport.resolution = (200, 112)
    # viewport.resolution = (5120 , 2880)
