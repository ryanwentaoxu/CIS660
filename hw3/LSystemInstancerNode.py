# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random
import LSystem
import math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "LSystemInstancerNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition

class LSystemInstancerNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()

    # I refer to the Maya API Programming tutorial: https://www.chadvernon.com/maya-api-programming/
    angle = OpenMaya.MObject()
    step_size = OpenMaya.MObject()
    grammar_file = OpenMaya.MObject()
    iterations = OpenMaya.MObject()

    outBranches = OpenMaya.MObject()
    outFlowers = OpenMaya.MObject()

    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should
        #         take in three floats for max position (X,Y,Z), three floats
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData.
        if plug == LSystemInstancerNode.outBranches or plug == LSystemInstancerNode.outFlowers:
            """
            input
            """
            angle_val = data.inputValue(LSystemInstancerNode.angle).asFloat()
            step_size_val = data.inputValue(LSystemInstancerNode.step_size).asFloat()
            grammar_file_val = data.inputValue(LSystemInstancerNode.grammar_file).asString()
            iterations_val = data.inputValue(LSystemInstancerNode.iterations).asInt()
            """
            output
            """

            """
            branch: We need to oreint the branches of LSystem, so we add scale and aimDirection
            """
            outBranchesData = data.outputValue(LSystemInstancerNode.outBranches)
            outBranchesAAD = OpenMaya.MFnArrayAttrsData()
            outBranchesObject = outBranchesAAD.create()
            branchesPositionArray = outBranchesAAD.vectorArray("position")
            branchesIdArray = outBranchesAAD.doubleArray("id")
            branchesScaleArr = outBranchesAAD.vectorArray("scale")
            branchesAimDArray = outBranchesAAD.vectorArray("aimDirection")

            """
            flower
            """
            outFlowersData = data.outputValue(LSystemInstancerNode.outFlowers)
            outFlowersAAD = OpenMaya.MFnArrayAttrsData()
            outFlowersObject = outFlowersAAD.create()
            flowersPositionArray = outFlowersAAD.vectorArray("position")
            flowersIdArray = outFlowersAAD.doubleArray("id")

            """
            initialize the l system
            """
            l_system = LSystem.LSystem()

            l_system.loadProgram(str(grammar_file_val))
            l_system.setDefaultAngle(angle_val)
            l_system.setDefaultStep(step_size_val)

            """
            from instruction, we can use VectorPyBranch to initialize a vector branches to be filled by the process function
            """
            branches = LSystem.VectorPyBranch()
            flowers = LSystem.VectorPyBranch()

            l_system.processPy(iterations_val, branches, flowers)

            # Loop to fill the arrays:
            for i in range(len(branches)):
                ad = OpenMaya.MVector(branches[i][3] - branches[i][0], branches[i][4] - branches[i][1], branches[i][5] - branches[i][2])
                pos = OpenMaya.MVector((branches[i][3] + branches[i][0]) / 2.0, (branches[i][4] + branches[i][1]) / 2.0, (branches[i][5] + branches[i][2]) / 2.0)
                norm = calculate_norm((branches[i][3] - branches[i][0], branches[i][4] - branches[i][1], branches[i][5] - branches[i][2]))
                branchesPositionArray.append(pos)
                branchesIdArray.append(i)
                branchesScaleArr.append(OpenMaya.MVector(norm, 1, 1))
                branchesAimDArray.append(ad)

            for i in range(len(flowers)):
                pos = OpenMaya.MVector(flowers[i][0], flowers[i][1], flowers[i][2])
                flowersPositionArray.append(pos)
                flowersIdArray.append(i)


            outBranchesData.setMObject(outBranchesObject)
            outFlowersData.setMObject(outFlowersObject)
        data.setClean(plug)

def calculate_norm(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])



# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the
    #         MAKE_INPUT and MAKE_OUTPUT functions.

    # here I refer to the tutorial https://www.chadvernon.com/maya-api-programming/
    LSystemInstancerNode.angle = nAttr.create("angle", "a", OpenMaya.MFnNumericData.kFloat, 10.0)
    LSystemInstancerNode.step_size = nAttr.create("step_size", "ss", OpenMaya.MFnNumericData.kFloat, 1.0)
    default_file = "C:\Users\cassi\cis660\hw3\HW3_basecode-2022(1)\HW3_basecode_VS2017\plants\\flower1.txt"
    LSystemInstancerNode.grammar_file = tAttr.create("grammar_file", "gf", OpenMaya.MFnData.kString, OpenMaya.MFnStringData().create(default_file))
    LSystemInstancerNode.iterations = nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kInt, 3)
    MAKE_INPUT(nAttr)

    LSystemInstancerNode.outBranches = tAttr.create("outBranches", "ob",  OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    LSystemInstancerNode.outFlowers = tAttr.create("outFlowers", "of",  OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        # print "Initialization!\n"
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.angle)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.step_size)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.grammar_file)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.iterations)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.outBranches)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.outFlowers)
        """
        add affect
        """
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle, LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle, LSystemInstancerNode.outFlowers)

        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.step_size, LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.step_size, LSystemInstancerNode.outFlowers)

        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations, LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations, LSystemInstancerNode.outFlowers)

        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.grammar_file ,LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.grammar_file ,LSystemInstancerNode.outFlowers)
    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstancerNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )
    
    mel_path = mplugin.loadPath() + "/menu.mel"
    file = open(mel_path,"r")
    mel_pl = file.read().replace("\n", "")
    OpenMaya.MGlobal.executeCommand(mel_pl)

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
