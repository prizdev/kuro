# Blender Server 3.0 - Project Kuro

import bpy
import sys
import os

def main():
    filesIn   = initInputs(0)
    resNogl   = initInputs(1)
    resGif    = initInputs(2)
    taskname  = initInputs(3)
    workDir   = initInputs(4)
    print(workDir)
    importAssets(filesIn, workDir)
    materialAssignment(filesIn)
    renderScene(resNogl, taskname, workDir, False)
    renderScene(resGif, taskname, workDir, True)
    processNogl(taskname, workDir)
    processGif(taskname, resGif, workDir)
    print('{ taskname : %s }' % taskname)
    print('Finished script!')


def initInputs(outputSwitch):
    taskname = str(sys.argv[sys.argv.index('-t') + 1])
    resNogl  = int(sys.argv[sys.argv.index('-nogl') + 1])
    resGif   = int(sys.argv[sys.argv.index('-gif') + 1])
    workDir  = str(os.getcwd())
    if sys.platform == 'linux2' or sys.platform == 'linux':
        assetsFolder = workDir + '/assets/%s/input/' % taskname
    else:
        assetsFolder = workDir + '\\assets\\%s\\input\\' % taskname
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
    else:
        return(workDir)

def importAssets(filesIn, workDir):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        bpy.ops.wm.open_mainfile(filepath = workDir + '/assets/blueprintBlend/blueprint_v001_003.blend')
    else:
        bpy.ops.wm.open_mainfile(filepath = workDir + '\\assets\\blueprintBlend\\blueprint_v001_003.blend')
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


def renderScene(resolution, taskname, workDir, gifBool):
    if gifBool == True:
        bpy.data.scenes['Scene'].frame_start = 82
        bpy.data.scenes['Scene'].frame_end   = 382
    else:
        bpy.data.scenes['Scene'].frame_start = 1
        bpy.data.scenes['Scene'].frame_end   = 81

    render = bpy.data.scenes['Scene'].render
    render.resolution_x = resolution * 2
    render.resolution_y = resolution * 2

    if sys.platform == 'linux2' or sys.platform == 'linux':
        render.filepath = workDir + '/assets/%s/render/' % taskname
    else:
        render.filepath = workDir + '\\assets\\%s\\render\\' % taskname
    bpy.ops.render.render(animation = True, write_still = True)


def processNogl(taskname, workDir):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        imgFiles = os.listdir(workDir + '/assets/%s/render' % taskname)
    else:
        imgFiles = os.listdir(workDir + '\\assets\\%s\\render' % taskname)
    noglFiles    = []
    indices      = []
    rowList      = [1, 17, 33, 49, 65, 81]
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

    noglFiles = sorted(noglFiles)
    trmCmd = 'convert ( '
    for n in range(1, 6):
        for x in noglFiles[rowList[n - 1]:rowList[n]]:
            trmCmd = trmCmd + '%s -resize 512x512 ' % x
            if x == noglFiles[rowList[5] - 1]:
                trmCmd = trmCmd + '+append )'
            elif x == noglFiles[rowList[n] - 1]:
                trmCmd = trmCmd + '+append ) ( '
            else:
                pass



    if sys.platform == 'linux2' or sys.platform == 'linux':
        trmCmd = trmCmd + ' -append %sspritesheet%s.jpg' % (workDir + '/assets/%s/output/' % taskname, taskname)
        trmCmd = trmCmd.replace('(', '"("');
        trmCmd = trmCmd.replace(')', '")"');
        os.chdir(workDir + '/assets/%s/render' % taskname)
    else:
        trmCmd = trmCmd + ' -append %sspritesheet%s.jpg' % (workDir + '\\assets\\%s\\output\\' % taskname, taskname)
        os.chdir(workDir + '\\assets\\%s\\render' % taskname)
    os.system(trmCmd)


def processGif(taskname, resGif, workDir):
    if sys.platform == 'linux2' or sys.platform == 'linux':
        imgFiles = os.listdir(workDir + '/assets/%s/render' % taskname)
    else:
        imgFiles = os.listdir(workDir + '\\assets\\%s\\render' % taskname)
    gifFilesList = []
    gifFiles     = ''
    indices      = []
    for index in range(82, 602):
        if len(str(index)) == 1:
            indices.append('000%s' % str(index))
        elif len(str(index)) == 2:
            indices.append('00%s' % str(index))
        else:
            indices.append('0%s' % str(index))

    for img in imgFiles:
        for index in indices:
            if img.find(index) != -1:
                gifFilesList.append(img)

    gifFilesList = sorted(gifFilesList)
    for gifFile in gifFilesList:
        gifFiles = gifFiles + gifFile + ' '

    if sys.platform == 'linux2' or sys.platform == 'linux':
        os.chdir(workDir + '/assets/%s/render' % taskname)
        os.system('convert -layers OptimizePlus -delay 3x100 ' + gifFiles + '-loop 0 %sanimation%s.gif' % (workDir + '/assets/%s/output/' % taskname, taskname))
    else:
        os.chdir(workDir + '\\assets\\%s\\render' % taskname)
        os.system('convert -layers OptimizePlus -delay 3x100 ' + gifFiles + '-loop 0 %sanimation%s.gif' % (workDir + '\\assets\\%s\\output\\' % taskname, taskname))



if __name__ == "__main__":
    main()
