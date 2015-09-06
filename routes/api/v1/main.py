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
    processNogl(taskname)
    print('{ taskname : %s }' % taskname)
    print('Finished script!')


def initInputs(outputSwitch):
    taskname = str(sys.argv[sys.argv.index('-t') + 1])
    resNogl  = int(sys.argv[sys.argv.index('-nogl') + 1])
    resGif   = int(sys.argv[sys.argv.index('-gif') + 1])
    if sys.platform == 'linux2' or sys.platform == 'linux':
        assetsFolder = os.getcwd() + '/assets/%s/input/' % taskname
    else:
        assetsFolder = os.getcwd() + '\\assets\\%s\\input\\' % taskname
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
    else:
        return(taskname)
print(os.getcwd())

def importAssets(filesIn):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        bpy.ops.wm.open_mainfile(filepath = os.getcwd() + '/assets/blueprintBlend/blueprint_v001_003.blend')
    else:
        bpy.ops.wm.open_mainfile(filepath = os.getcwd() + '\\assets\\blueprintBlend\\blueprint_v001_003.blend')
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
        render.filepath = os.getcwd() + '/assets/%s/render/render.jpg' % taskname
    else:
        render.filepath = os.getcwd() + '\\assets\\%s\\render\\render.jpg' % taskname
    bpy.ops.render.render(animation = True, write_still = True)


def processNogl(taskname):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        imgFiles = (os.listdir(os.getcwd() + '/assets/%s/render' % taskname))

    else:
        imgFiles    = os.listdir(os.getcwd() + '\\assets\\%s\\render' % taskname)
        noglFiles   = []
        indices     = []
        rowList      = [0, 16, 32, 48, 64, 80]
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
        for x in range(1, 7):
            n = rowList[x - 1]
            while n <= x:
                for noglFile in noglFiles:
                    trmCmd = trmCmd + '%s -resize 512x512 ' % noglFile
                    n += 1
            trmCmd = trmCmd + '+append ) '
        trmCmd = trmCmd + '-append spritesheet%s.jpg' % taskname
        print(trmCmd)

        os.chdir(os.getcwd() + '\\assets\\123456\\render')






if __name__ == "__main__":
    main()
