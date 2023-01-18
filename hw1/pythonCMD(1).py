import sys

# Imports to use the Maya Python API
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Import the Python wrappers for MEL commands
import maya.cmds as cmds

# The name of the command. 
kPluginCmdName = "pyHelloMaya"

class helloMayaCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, argList):
        # TODO fill in this code to implement the command.
        syntax = OpenMaya.MSyntax()
        syntax.addFlag("-n", "-name", OpenMaya.MSyntax.kString)
        syntax.addFlag("-id", "identi", OpenMaya.MSyntax.kString)
        name = ""
        iden = ""
        argData = OpenMaya.MArgParser(syntax, argList)
        if argData.isFlagSet("-name"):
        	name = argData.flagArgumentString("-name", 0)
        if argData.isFlagSet("-id"):
        	iden = argData.flagArgumentString("-id", 0)
        cmds.confirmDialog( title='Hello Maya Python', message='Name:' + name + "\n" + "id:"+ iden, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
        self.setResult("Executed command")

# Create an instance of the command.
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(helloMayaCommand())

# Initialize the plugin
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "cg@penn", "1.0", "2012")
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise

# Uninitialize the plugin
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
        raise