# hints on the major modification of saba viewer library

## stage one 

### main modification source

we need to check /media/root/help/pyjom/tests/mmd_human_dance_pose/saba/viewer/Saba/Viewer/Viewer.cpp since it has commands that can be initiated by lua scripts. we may check how to implement recording since it will be async. we better have the recording length passed to the command beforehand otherwise we will certainly fail.

if not passed the value it will be marked at when the model stops moving, or will we be able to know that?

the primary functions are viewer.Initialize(viewerInitParam) and viewer.ExecuteCommand(viewerCommand). we had better know how to change camera position too, but that may require some sleep or some overheads? extra params?

viewer.Run() is to start the main viewer loop.

### initial practices

find out how to record the glfw window from /media/root/help/pyjom/tests/mmd_human_dance_pose/saba/example/simple_mmd_viewer_glfw.cpp