import bpy, sys, os, re

def main():
    directory = initInputs(0)
    nogl      = initInputs(1)
    gif       = initInputs(2)
    taskname  = initInputs(3)

    initProject(directory, taskname)
    renderScene(nogl, 'nogl', directory, taskname)
    renderScene(gif, 'gif', directory, taskname)
    processNogl(directory, taskname)
    processGif(directory, taskname)

    print('Finished script!')


def initInputs(switch):
    directory = os.getcwd().replace('\\', '/')

    taskname = int(sys.argv[sys.argv.index('-t') + 1])

    if '-nogl' in sys.argv:
        nogl = int(sys.argv[sys.argv.index('-nogl') + 1])
    else:
        nogl = 0

    if '-gif' in sys.argv:
        gif = int(sys.argv[sys.argv.index('-gif') + 1])
    else:
        gif = 0

    if switch == 0:
        return(directory)
    elif switch == 1:
        return(nogl)
    elif switch == 2:
        return(gif)
    elif switch == 3:
        return(taskname)


def initProject(directory, taskname):
    bpy.ops.wm.open_mainfile(filepath = directory + '/assets/blueprintBlend/blueprint_v001_005.blend')
    bpy.ops.import_scene.obj(filepath = directory + '/assets/%s/input/geometry.obj' % taskname)

    for obj in bpy.data.objects:
        if 'Cube' != obj.name and 'fulcrum' != obj.name and 'Camera' != obj.name:
            obj.data.materials[0] = bpy.data.materials['Material']

    mat                = bpy.data.materials['Material']
    nodes              = mat.node_tree.nodes
    node_texture       = bpy.data.materials['Material'].node_tree.nodes[5]
    emission_shader    = bpy.data.materials['Material'].node_tree.nodes[2]
    node_texture.image = bpy.data.images.load(directory + '/assets/%s/input/diffuse.jpg' % taskname)
    links              = mat.node_tree.links
    link               = links.new(node_texture.outputs[0], emission_shader.inputs[0])


def renderScene(resolution, output, directory, taskname):
    if resolution != 0:
        if output == 'gif':
            bpy.data.scenes['Scene'].frame_start = 82
            bpy.data.scenes['Scene'].frame_end   = 381
        else:
            bpy.data.scenes['Scene'].frame_start = 2
            bpy.data.scenes['Scene'].frame_end   = 81

        render = bpy.data.scenes['Scene'].render
        render.resolution_x = resolution * 2
        render.resolution_y = resolution * 2
        render.filepath = directory + '/assets/%s/render/%s/' % (taskname, output)
        bpy.ops.render.render(animation = True, write_still = True)


def processNogl(directory, taskname):
    images = os.listdir(directory + '/assets/%s/render/nogl/' % taskname)
    rowList = [0, 16, 32, 48, 64, 80]
    trmCmd = 'convert ( '
    for n in range(0, 5):
        for image in images[rowList[n]:rowList[n + 1]]:
            trmCmd = trmCmd + '%s -resize 512x512 ' % image
            if image == images[rowList[5] - 1]:
                trmCmd = trmCmd + '+append )'
            elif image == images[rowList[n] + 15]:
                trmCmd = trmCmd + '+append ) ( '
    trmCmd = trmCmd + ' -append %sspritesheet.jpg' % (directory + '/assets/%s/output/' % taskname)
    if sys.platform == 'linux2' or sys.platform == 'linux':
        trmCmd = trmCmd.replace('(', '"("');
        trmCmd = trmCmd.replace(')', '")"');

    os.chdir(directory + '/assets/%s/render/nogl/' % taskname)
    os.system(trmCmd)


def processGif(directory, taskname):
    images = os.listdir(directory + '/assets/%s/render/gif/' % taskname)
    imageString = ''
    for image in images:
        imageString = imageString + image + ' '
    trmCmd = 'convert -layers OptimizePlus -delay 3x100 %s-loop 0 %sanimation.gif' % (imageString, directory + '/assets/%s/output/' % taskname)

    os.chdir(directory + '/assets/%s/render/gif/' % taskname)
    os.system(trmCmd)


main()
