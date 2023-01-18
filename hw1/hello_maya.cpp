#include "hello_maya.h"
#include <maya/MFnPlugin.h>
// define EXPORT for exporting dll functions
#define EXPORT _declspec(dllexport)
// Maya Plugin creator function
void *helloMaya::creator()
{
	return new helloMaya;
}
// Plugin doIt function
MStatus helloMaya::doIt(const MArgList& argList)
{
	MStatus status;
	MGlobal::displayInfo("Hello World!");
	// <<<your code goes here>>>
	// MString name = argList.asString(0);
	// MString year = argList.asString(1);
	// MString semester = argList.asString(2);
	// MString id = argList.asString(3);
	MSyntax syntax;
	status = syntax.addFlag("-n", "-name", MSyntax::kString);
	status = syntax.addFlag("-id", "-identy", MSyntax::kString);
	MArgParser argData(syntax, argList, &status);
	MString name;
	MString id;
	if (argData.isFlagSet("-name"))
	{
		status = argData.getFlagArgument("-name", 0, name);
	}
	if (argData.isFlagSet("-name"))
	{
		status = argData.getFlagArgument("-id", 0, id);
	}
	MString dialogBoxWindow = "confirmDialog -title \"Hello Maya\" -message \"Name:" + name +"\\nID:" + id + "\"" + " -button \"OK\"-defaultButton \"OK\" -dismissString \"OK\"";
	// MGlobal::displayInfo(dialogBoxWindow);
	status = MGlobal::executeCommand(dialogBoxWindow);
	return status;
}
// Initialize Maya Plugin upon loading
EXPORT MStatus initializePlugin(MObject obj)
{
	MStatus status;
	MFnPlugin plugin(obj, "CIS660", "1.0", "Any");
	status = plugin.registerCommand("helloMaya", helloMaya::creator);
	if (!status)
		status.perror("registerCommand failed");
	return status;
}
// Cleanup Plugin upon unloading
EXPORT MStatus uninitializePlugin(MObject obj)
{
	MStatus status;
	MFnPlugin plugin(obj);
	status = plugin.deregisterCommand("helloMaya");
	if (!status)
		status.perror("deregisterCommand failed");
	return status;
}