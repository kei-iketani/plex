#*********************************************************************
# content   = sets the name of all shader groups as the shader (+SG)
# version   = 0.1.0
# date      = 2019-12-01

# license   = MIT
# author    = Alexander Richter <alexanderrichtertd.com>
#*********************************************************************


import os

import maya.mel as mel
import maya.cmds as cmds
from pymel.core import *

import pipelog


#*********************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = pipelog.init(script=TITLE)


#*********************************************************************
# FUNCTIONS
def sg_from_material(material):
    material = PyNode(material)
    return material.shadingGroups()


def start(shader_types=["alSurface", "alLayer"]):
    shaders = []

    for shader_type in shader_types:
        shaders += cmds.ls(type = shader_type)

    for shader in shaders:
        shader_groups = sg_from_material(shader)

        if len(shader_groups) == 0:
            continue

        #START: ADDING
        shader_group = shader_groups[0]
        own_shader_roups = []
        conns = connectionInfo(PyNode(shader).outColor, destinationFromSource = True)

        for conn in conns:
            connNode = PyNode(conn).node()

            if PyNode(connNode).nodeType() != "shadingEngine":
                continue
            else:
                own_shader_roups.append(str(connNode))

        if not (shader_group in own_shader_roups):
            continue
        # END: ADDING

        if (shader_group != shader + "SG"):
            try:
                mel.eval('rename ' + shader_group + ' ' + shader + 'SG;')
            except:
                LOG.error("** FAIL | Unite Shader and Shader Group: Shader has no shading group or is a reference - " + shader + " **")

    LOG.info("DONE : Unite Shader and Shader Group")
