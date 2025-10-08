import maya.cmds as cmds

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


# Window
def show_custom_tool():
    window_id = "IamGrid"
    if cmds.workspaceControl(window_id, q=True, exists=True):
        cmds.deleteUI(window_id, control=True)

    cmds.workspaceControl(window_id, label="You are now under UE grid size", retain=False)
    
    #buttons layout
    cmds.rowLayout(numberOfColumns=5,columnWidth=[(1, 10), (2, 55), (3, 55), (4, 55)],)

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


# Set grid to UE size
cmds.grid(reset=True)
cmds.grid(size=2000, spacing=100, divisions=2)

# Run the tool
show_custom_tool()
