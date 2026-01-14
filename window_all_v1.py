import maya.cmds as cmds
import os
import re

# functions
def create_custom_cube(*args):
    cube = cmds.polyCube(name="pCube")[0]
    cmds.scale(100, 100, 100, cube)
    cmds.makeIdentity(cube, apply=True, t=1, r=1, s=1, n=0)
    cmds.delete(cube, ch=True)
    cmds.select(cube)

def create_custom_sphere(*args):
    sphere = cmds.polySphere(name="pSphere")[0]
    cmds.scale(100, 100, 100, sphere)
    cmds.makeIdentity(sphere, apply=True, t=1, r=1, s=1, n=0)
    cmds.delete(sphere, ch=True)
    cmds.select(sphere)

def create_custom_cylinder(*args):
    cylinder = cmds.polyCylinder(name="pCylinder")[0]
    cmds.scale(100, 100, 100, cylinder)
    cmds.makeIdentity(cylinder, apply=True, t=1, r=1, s=1, n=0)
    cmds.delete(cylinder, ch=True)
    cmds.select(cylinder)
    
def create_custom_nurbs_circle(*args):
    circle = cmds.circle(name="nurbsCircle", normal=[0,1,0], radius=1)[0]
    cmds.scale(100, 100, 100, circle)
    cmds.makeIdentity(circle, apply=True, t=1, r=1, s=1, n=0)
    cmds.delete(circle, ch=True)
    cmds.select(circle)

def set_grid_to_ue_size(*args):
    cmds.grid(size=2000, spacing=100, divisions=2)

def reset_grid(*args):
    cmds.grid(reset=True)

def zero_scale_this_frame(*args):
    sel = cmds.ls(selection=True)
    if not sel or len(sel) != 1:
        cmds.warning("Please select a single object.")
        return

    obj = sel[0]
    current_frame = cmds.currentTime(query=True)
    prev_frame = current_frame - 1

    # Get previous frame scale values
    prev_scale = []
    for axis in ['X', 'Y', 'Z']:
        attr = f"{obj}.scale{axis}"
        prev_scale.append(cmds.getAttr(attr, time=prev_frame))

    # Set keyframe at previous frame (only scale channels)
    for i, axis in enumerate(['X', 'Y', 'Z']):
        cmds.setKeyframe(obj, attribute=f"scale{axis}", time=prev_frame, value=prev_scale[i])

    # Set scale to 0 at current frame and keyframe
    for axis in ['X', 'Y', 'Z']:
        attr = f"{obj}.scale{axis}"
        cmds.setAttr(attr, 0)
        cmds.setKeyframe(obj, attribute=f"scale{axis}", time=current_frame, value=0)

def one_scale_this_frame(*args):
    sel = cmds.ls(selection=True)
    if not sel or len(sel) != 1:
        cmds.warning("Please select a single object.")
        return

    obj = sel[0]
    current_frame = cmds.currentTime(query=True)
    prev_frame = current_frame - 1

    # Set scale to 0 at previous frame and keyframe
    for axis in ['X', 'Y', 'Z']:
        attr = f"{obj}.scale{axis}"
        cmds.setAttr(attr, 0)
        cmds.setKeyframe(obj, attribute=f"scale{axis}", time=prev_frame, value=0)

    # Set scale to 1 at current frame and keyframe
    for axis in ['X', 'Y', 'Z']:
        attr = f"{obj}.scale{axis}"
        cmds.setAttr(attr, 1)
        cmds.setKeyframe(obj, attribute=f"scale{axis}", time=current_frame, value=1)

def smart_versioned_save(*args):
    VERSION_PATTERN = re.compile(r"v(\d{3})")
    scene_path = cmds.file(q=True, sceneName=True)

    # if never saved
    if not scene_path:
        cmds.confirmDialog(title="Save by hand first", message="Scene has never been saved. Please save the first version by hand.", button=["OK"])
        return

    #get paths
    dir_path = os.path.dirname(scene_path)
    file_name = os.path.basename(scene_path)
    base, ext = os.path.splitext(file_name)
    ext = ext.lstrip(".")

    matches = list(VERSION_PATTERN.finditer(base))
    #match the version  
    if matches:
        last_match = matches[-1]
        old_version = int(last_match.group(1))
        new_version = f"{old_version + 1:03d}"

        new_base = (
            base[:last_match.start(1)]
            + new_version
            + base[last_match.end(1):]
        )
    else:
        new_base = f"{base}_v001"

    default_path = os.path.join(dir_path, f"{new_base}.{ext}")

    #pop up window
    result = cmds.fileDialog2(
        fileMode=0,
        caption="Save Versioned Scene",
        startingDirectory=default_path,
        fileFilter="Maya Files (*.ma *.mb)"
    )
    # it will return a path, if cancelled it returns None
    if not result:
        return
    
    #here is where it actually saves, the window is just a double check kinda thing
    cmds.file(rename=result[0])
    cmds.file(save=True)

    cmds.inViewMessage(
        amg=f"<hl>Saved:</hl> {os.path.basename(result[0])}",
        pos="topCenter",
        fade=True
    )

# Window
def show_custom_tool():
    window_id = "IamGruid"
    if cmds.workspaceControl(window_id, q=True, exists=True):
        cmds.deleteUI(window_id, control=True)

    cmds.workspaceControl(window_id, label="UE Grid Size Tool", retain=False)
    cmds.columnLayout(adjustableColumn=True)

    cmds.rowLayout(numberOfColumns=5, columnWidth=[(1, 10), (2, 55), (3, 55), (4, 55)])
    cmds.text(label="")
    cmds.iconTextButton(
        style='iconAndTextVertical',
        image1='polyCube.png',
        label='Cube',
        command=create_custom_cube
    )
    cmds.iconTextButton(
        style='iconAndTextVertical',
        image1='polySphere.png',
        label='Sphere',
        command=create_custom_sphere
    )
    cmds.iconTextButton(
        style='iconAndTextVertical',
        image1='polyCylinder.png',
        label='Cylinder',
        command=create_custom_cylinder
    )
    cmds.iconTextButton(
        style='iconAndTextVertical',
        image1='circle.png',
        label='NurbsCircle',
        command=create_custom_nurbs_circle
    )
    cmds.setParent('..')

    cmds.separator(height=10, style='in')

    cmds.frameLayout(label="Set/Reset Grid Size", collapsable=True, collapse=True, marginWidth=10, marginHeight=5)
    cmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 150), (2, 150)])
    cmds.button(label="Set Grid to UE Size", command=set_grid_to_ue_size)
    cmds.button(label="Reset Grid", command=reset_grid)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='in')
    cmds.frameLayout(label="Hide/Show Keyframe", collapsable=True, collapse=True, marginWidth=10, marginHeight=5)
    cmds.rowLayout(numberOfColumns=2, columnWidth=[(1, 150), (2, 150)])
    cmds.button(label="Key Hide", command=zero_scale_this_frame)
    cmds.button(label="Key Show", command=one_scale_this_frame)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='in')
    
    cmds.button(label="Smart Versioned Save", command=smart_versioned_save)
    
    cmds.setParent('..')
    

# Set grid to UE size
reset_grid()
set_grid_to_ue_size()

# Run the tool
show_custom_tool()
