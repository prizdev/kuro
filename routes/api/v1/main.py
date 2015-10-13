import bpy, sys, os, re

def main():
    directory = initInputs(0)
    nogl      = initInputs(1)
    gif       = initInputs(2)

    initProject(directory)
    renderScene(nogl, 'nogl', directory)
    renderScene(gif, 'gif', directory)
    processNogl(directory)
    processGif(directory)

    print('Finished script!')


def initInputs(switch):
    directory = os.getcwd().replace('\\', '/')

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


def initProject(directory):
    bpy.ops.wm.open_mainfile(filepath = directory + '/assets/blueprintBlend/blueprint_v001_005.blend')
    bpy.ops.import_scene.obj(filepath = directory + '/assets/input/geometry.obj')

    for obj in bpy.data.objects:
        if 'Cube' != obj.name and 'fulcrum' != obj.name and 'Camera' != obj.name:
            obj.data.materials[0] = bpy.data.materials['Material']

    mat                = bpy.data.materials['Material']
    nodes              = mat.node_tree.nodes
    node_texture       = bpy.data.materials['Material'].node_tree.nodes[5]
    emission_shader    = bpy.data.materials['Material'].node_tree.nodes[2]
    node_texture.image = bpy.data.images.load(directory + '/assets/input/diffuse.jpg')
    links              = mat.node_tree.links
    link               = links.new(node_texture.outputs[0], emission_shader.inputs[0])


def renderScene(resolution, output, directory):
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
        render.filepath = directory + '/assets/render/%s/' % output
        bpy.ops.render.render(animation = True, write_still = True)


def processNogl(directory):
    images = os.listdir(directory + '/assets/render/nogl/')
    rowList = [0, 16, 32, 48, 64, 80]
    trmCmd = 'convert ( '
    for n in range(0, 5):  #range(0,5) are the indices of rowList, [0, 1, 2, 3, 4]
        for image in images[rowList[n]:rowList[n + 1]]:
            trmCmd = trmCmd + '%s -resize 512x512 ' % image
            if image == images[rowList[5] - 1]:
                trmCmd = trmCmd + '+append )'
            elif image == images[rowList[n] + 15]:
                trmCmd = trmCmd + '+append ) ( '
    trmCmd = trmCmd + ' -append %sspritesheet.jpg' % (directory + '/assets/output/')
    if sys.platform == 'linux2' or sys.platform == 'linux':
        trmCmd = trmCmd.replace('(', '"("');
        trmCmd = trmCmd.replace(')', '")"');

    try:
        os.mkdir(directory + '/assets/output/')
    except:
        pass
    os.chdir(directory + '/assets/render/nogl/')
    os.system(trmCmd)


def processGif(directory):
    images = os.listdir(directory + '/assets/render/gif/')
    imageString = ''
    for image in images:
        imageString = imageString + image + ' '
    trmCmd = 'convert -layers OptimizePlus -delay 3x100 %s-loop 0 %sanimation.gif' % (imageString, directory + '/assets/output/')

    try:
        os.mkdir(directory + '/assets/output/')
    except:
        pass
    os.chdir(directory + '/assets/render/gif/')
    os.system(trmCmd)


main()
