import bpy, sys, os

def main():
    directory = os.getcwd().replace('\\', '/') #Must be working in the kuro directory
    taskname = int(sys.argv[sys.argv.index('-t') + 1]) #Set taskname via command line using -t
    if '-nogl' in sys.argv: #Set nogl viewer resolution via command line using -nogl
        nogl = int(sys.argv[sys.argv.index('-nogl') + 1])
    else:
        nogl = 0
    if '-gif' in sys.argv: #Set gif resoution via command line using -gif
        gif = int(sys.argv[sys.argv.index('-gif') + 1])
    else:
        gif = 0

    initProject(directory, taskname)
    renderScene(nogl, 'nogl', directory, taskname)
    renderScene(gif, 'gif', directory, taskname)
    processNogl(directory, taskname)
    processGif(directory, taskname)

    print('Finished script!')


def initProject(directory, taskname):
    #Opens a Blender file from the kuro directory containing animation and shader information
    bpy.ops.wm.open_mainfile(filepath = directory + '/assets/blueprintBlend/blueprint_v001_005.blend')
    #Imports OBJ asset
    bpy.ops.import_scene.obj(filepath = directory + '/assets/%s/input/geometry.obj' % taskname)

    #If an object in the scene is not called Cube, fulcrum, or camera, it is the imported OBJ.  Assign it 'Material'.
    exlusion = ('Cube', 'fulcrum', 'Camera')
    for obj in bpy.data.objects:
        if obj.name not in exclusion:
            obj.data.materials[0] = bpy.data.materials['Material']

    #Import the diffuse texture and assign it to the emission color of 'Material'
    mat                = bpy.data.materials['Material']
    nodes              = mat.node_tree.nodes
    nodeTexture        = bpy.data.materials['Material'].node_tree.nodes[5]
    emissionShader     = bpy.data.materials['Material'].node_tree.nodes[2]
    nodeTexture.image  = bpy.data.images.load(directory + '/assets/%s/input/diffuse.jpg' % taskname)
    links              = mat.node_tree.links
    link               = links.new(nodeTexture.outputs[0], emissionShader.inputs[0])


def renderScene(resolution, output, directory, taskname):
    #Animations for the nogl and gif are predefined on specific frames in the blender file
    if resolution != 0:
        if output == 'gif':
            bpy.data.scenes['Scene'].frame_start = 82
            bpy.data.scenes['Scene'].frame_end   = 381
        else:
            bpy.data.scenes['Scene'].frame_start = 2
            bpy.data.scenes['Scene'].frame_end   = 81

        #Set resolution and begin rendering
        render = bpy.data.scenes['Scene'].render
        render.resolution_x = resolution * 2
        render.resolution_y = resolution * 2
        render.filepath = directory + '/assets/%s/render/%s/' % (taskname, output)
        bpy.ops.render.render(animation = True, write_still = True)


def processNogl(directory, taskname):
    #Executes Imagemagick processes via command line
    images = os.listdir(directory + '/assets/%s/render/nogl/' % taskname) #Get a list of rendered frames
    images.reverse()
    rows = [0, 16, 32, 48, 64, 80]
    trmCmd = 'convert ( '
    for n in range(0, 5):
        for image in images[rows[n]:rows[n + 1]]: #For each image in a row
            trmCmd += '%s -resize 512x512 ' % image #Standard syntax for appending images in Imagemagick
            if image == images[rows[5] - 1]:
                trmCmd += '+append )' #If the last row and column are reached, close parentheses
            elif image == images[rows[n] + 15]:
                trmCmd += '+append ) ( ' #If the end of a row is reached, start a new row
    trmCmd += ' -append %sspritesheet.jpg' % (directory + '/assets/%s/output/' % taskname) #Set output directory
    if sys.platform == 'linux2' or sys.platform == 'linux': #Linux requires a slight syntax modification
        trmCmd = trmCmd.replace('(', '"("');
        trmCmd = trmCmd.replace(')', '")"');

    os.chdir(directory + '/assets/%s/render/nogl/' % taskname) #CD to the nogl render directory
    os.system(trmCmd) #Run trmCmd in the command line


def processGif(directory, taskname):
    #Executes Imagemagick processes via command line
    images = os.listdir(directory + '/assets/%s/render/gif/' % taskname) #Get a list of rendered frames
    imageString = ''
    for image in images:
        imageString.append(image + ' ')
    #Create Imagemagick command
    trmCmd = 'convert -layers OptimizePlus -delay 3x100 %s-loop 0 %sanimation.gif' % (imageString, directory + '/assets/%s/output/' % taskname)

    os.chdir(directory + '/assets/%s/render/gif/' % taskname) #CD to the gif render directory
    os.system(trmCmd) #Run trmCmd in the command line


if __name__ == '__main__':
    main()
