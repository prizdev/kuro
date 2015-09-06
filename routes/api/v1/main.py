# Blender Server 3.0 - Project Kuro

import bpy
import sys
import os

def main():
    filesIn   = initInputs(0)
    resNogl   = initInputs(1)
    resGif    = initInputs(2)
    taskname  = initInputs(3)
    #importAssets(filesIn)
    #materialAssignment(filesIn)
    #renderScene(resNogl, False)
    #renderScene(resGif, True)
    processNogl(filesIn)
    print('{ taskname : %s }' % taskname)
    print('Finished script!')


def initInputs(outputSwitch):
    taskname = str(sys.argv[sys.argv.index('-t') + 1])
    resNogl  = int(sys.argv[sys.argv.index('-nogl') + 1])
    resGif   = int(sys.argv[sys.argv.index('-gif') + 1])
    if sys.platform == 'linux2' or sys.platform == 'linux':
        assetsFolder = '/home/tim/share/Prizmiq/Misc/Dev/Github/kuro/assets/%s/input/' % taskname
    else:
        assetsFolder = 'E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\%s\\input\\' % taskname
    fileNames    = ['geometry.obj', 'diffuse.jpg', 'specular.jpg', 'normal.jpg']    #specular and normal are not yet integrated
    filesIn      = []
    for name in fileNames:
        filesIn.append(assetsFolder + name)
    if outputSwitch == 0:
        return(filesIn)
    elif outputSwitch == 1:
        return(resNogl)
    elif outputSwitch == 2:
        return(resGif)
    elif outputSwitch == 3:
        return(taskname)


def importAssets(filesIn):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        bpy.ops.wm.open_mainfile(filepath = '/home/tim/share/Prizmiq/Misc/Dev/Github/kuro/assets/blueprintBlend/blueprint_v001_003.blend')
    else:
        bpy.ops.wm.open_mainfile(filepath = 'E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\blueprintBlend\\blueprint_v001_003.blend')
    bpy.ops.import_scene.obj(filepath = filesIn[0])


def materialAssignment(filesIn):
    for obj in bpy.data.objects:
        if 'Group' in obj.name:
            obj.data.materials[0] = bpy.data.materials['Material']

    mat                = bpy.data.materials['Material']
    nodes              = mat.node_tree.nodes
    node_texture       = bpy.data.materials['Material'].node_tree.nodes[5]
    emission_shader    = bpy.data.materials['Material'].node_tree.nodes[2]
    node_texture.image = bpy.data.images.load(filesIn[1])
    links              = mat.node_tree.links
    link               = links.new(node_texture.outputs[0], emission_shader.inputs[0])


def renderScene(resolution, gifBool):
    if gifBool == True:
        bpy.data.scenes['Scene'].frame_start = 82
        bpy.data.scenes['Scene'].frame_end   = 601
    else:
        bpy.data.scenes['Scene'].frame_start = 1
        bpy.data.scenes['Scene'].frame_end   = 81

    render = bpy.data.scenes['Scene'].render
    render.resolution_x = resolution * 2
    render.resolution_y = resolution * 2

    if sys.platform == 'linux2' or sys.platform == 'linux':
        render.filepath = '/home/tim/share/Prizmiq/Misc/Dev/Github/kuro/assets/123456/render/render.jpg'
    else:
        render.filepath = 'E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\123456\\render\\render.jpg'
    bpy.ops.render.render(animation = True, write_still = True)


def processNogl(filesIn):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        imgFiles = (os.listdir('/home/tim/share/Prizmiq/Misc/Dev/Github/kuro/assets/123456/render'))

    else:
        imgFiles    = os.listdir('E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\123456\\render')
        noglFiles   = []
        indices     = []
        for index in range(1, 82):
            if len(str(index)) == 1:
                indices.append('000%s' % str(index))
            elif len(str(index)) == 2:
                indices.append('00%s' % str(index))
            else:
                indices.append('0%s' % str(index))

        for img in imgFiles:
            for index in indices:
                if img.find(index) != -1:
                    noglFiles.append(img)

        trmCmd = 'convert ( '
        for noglFile in noglFiles:
            trmCmd = trmCmd + '%s -resize ' % noglFile
        print(trmCmd)

        os.chdir('E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\123456\\render')






if __name__ == "__main__":
    main()
