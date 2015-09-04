# Blender Server 3.0 - Project Kuro

import bpy
import os
import sys
import mathutils
import math


def main():
    filesIn = initInputs(0)
    resNogl = initInputs(1)
    resGif  = initInputs(2)
    importAssets(filesIn)
    materialAssignment(filesIn)
    renderScene(resNogl, False)
    renderScene(resGif, True)
    processOutput(filesIn)
    print('Finished script!')


def initInputs(outputSwitch):
    taskname = str(sys.argv[sys.argv.index('-t') + 1])
    resNogl  = int(sys.argv[sys.argv.index('-nogl') + 1])
    resGif   = int(sys.argv[sys.argv.index('-gif') + 1])
    assetsFolder = os.path.join('E:\\', 'Prizmiq', 'Misc', 'Dev', 'Github', 'kuro', 'assets', 'testFilepath', taskname, 'input')
    fileNames    = ['geometry.obj', 'diffuse.jpg', 'specular.jpg', 'normal.jpg']
    filesIn      = []
    for name in fileNames:
        filesIn.append(assetsFolder + '\\' + name)
    if outputSwitch == 0:
        return(filesIn)
    elif outputSwitch == 1:
        return(resNogl)
    else:
        return(resGif)


def importAssets(filesIn):
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

    render.filepath = 'E:\\Prizmiq\\Misc\\Dev\\Github\\kuro\\assets\\renderFilepath\\render.jpg'
    bpy.ops.render.render(animation = True, write_still = True)


def processOutput(filesIn):
    pass



if __name__ == "__main__":
    main()
