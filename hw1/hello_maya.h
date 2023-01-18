#ifndef HELLOMAYA_H
#define HELLOMAYA_H
#include <maya/MArgList.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>
#include <maya/msyntax.h>
#include <maya/MArgParser.h>

// custom Maya command
class helloMaya : public MPxCommand
{
public:
	helloMaya() {};
	virtual MStatus doIt(const MArgList& args);
	static void *creator();
	static MSyntax newSyntax();
};
#endif