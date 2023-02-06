# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random

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
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()

    # I refer to the Maya API Programming tutorial: https://www.chadvernon.com/maya-api-programming/
    # (a)
    inNumPoints = OpenMaya.MObject()
    # (b)
    x_min = OpenMaya.MObject()
    x_max = OpenMaya.MObject()
    y_min = OpenMaya.MObject()
    y_max = OpenMaya.MObject()
    z_min = OpenMaya.MObject()
    z_max = OpenMaya.MObject()
    # (c)
    outPoints =  OpenMaya.MObject()

    
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
        if plug == randomNode.outPoints:
            inNumPoints_val = data.inputValue(randomNode.inNumPoints).asInt()
            x_min_val = data.inputValue(randomNode.x_min).asFloat()
            x_max_val = data.inputValue(randomNode.x_max).asFloat()
            y_min_val = data.inputValue(randomNode.y_min).asFloat()
            y_max_val = data.inputValue(randomNode.y_max).asFloat()
            z_min_val = data.inputValue(randomNode.z_min).asFloat()
            z_max_val = data.inputValue(randomNode.z_max).asFloat()
            # below is from homework3 Appendix B
            pointsData = data.outputValue(randomNode.outPoints) #the MDataHandle
            pointsAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
            pointsObject = pointsAAD.create()
            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")
            # Loop to fill the arrays:
            for i in range(0, inNumPoints_val):
                x = random.uniform(x_min_val, x_max_val)
                y = random.uniform(y_min_val, y_max_val)
                z = random.uniform(z_min_val, z_max_val)
                current_pos = OpenMaya.MVector(x, y, z)
                positionArray.append(current_pos)
                idArray.append(i)
            pointsData.setMObject(pointsObject)
        data.setClean(plug)
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.

    # here I refer to the tutorial https://www.chadvernon.com/maya-api-programming/
    randomNode.inNumPoints = nAttr.create("inNumPoints", "n", OpenMaya.MFnNumericData.kInt, 11)
    randomNode.x_min = nAttr.create("x_min", "xi", OpenMaya.MFnNumericData.kFloat, 0.0)
    randomNode.x_max = nAttr.create("x_max", "xa", OpenMaya.MFnNumericData.kFloat, 10.0)
    randomNode.y_min = nAttr.create("y_min", "yi", OpenMaya.MFnNumericData.kFloat, 0.0)
    randomNode.y_max = nAttr.create("y_max", "ya", OpenMaya.MFnNumericData.kFloat, 10.0)
    randomNode.z_min = nAttr.create("z_min", "zi", OpenMaya.MFnNumericData.kFloat, 0.0)
    randomNode.z_max = nAttr.create("z_max", "za", OpenMaya.MFnNumericData.kFloat, 10.0)
    MAKE_INPUT(nAttr)

    randomNode.outPoints = tAttr.create("outPoints", "opo", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    print("breakpoint 1")

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
      
        print("Initialization!")
        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.x_min)
        randomNode.addAttribute(randomNode.x_max)
        randomNode.addAttribute(randomNode.y_min)
        randomNode.addAttribute(randomNode.y_max)
        randomNode.addAttribute(randomNode.z_min)
        randomNode.addAttribute(randomNode.z_max)
        randomNode.addAttribute(randomNode.outPoints)
        # add affects
        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.x_min, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.x_max, randomNode.outPoints) 
        randomNode.attributeAffects(randomNode.y_min, randomNode.outPoints) 
        randomNode.attributeAffects(randomNode.y_max, randomNode.outPoints) 
        randomNode.attributeAffects(randomNode.z_min, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.z_max, randomNode.outPoints)
    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )