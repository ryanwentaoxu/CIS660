#pragma once

#include <maya/MStringArray.h>
#include <maya/MTime.h>
#include <maya/MFnMesh.h>
#include <maya/MPoint.h>
#include <maya/MFloatPoint.h>
#include <maya/MFloatPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnPlugin.h>
#include <maya/MPxNode.h>
#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MFnMeshData.h>
#include <maya/MIOStream.h>
#include <maya/MPxCommand.h>
#include <string>
#include <maya/msyntax.h>
#include <maya/MArgParser.h>
#include <maya/MFnStringData.h>
#include "cylinder.h"
#include "LSystem.h"

class LSystemNode : public MPxNode
{
public:
	// constructor
	LSystemNode();
	// vitural destructor
	virtual ~LSystemNode();
	// static creator function
	static void* creator() { return new LSystemNode; };

	/*
	static MFnNumericAttribute angle_degree;
	static MFnNumericAttribute step_size;
	static MFnTypedAttribute grammar_file;
	static MFnUnitAttribute input_time;
	*/

	LSystem lsystem;

	static MTypeId id;
	// input time
	static MObject time;
	static MObject object_grammar;
	static MObject object_degree;
	static MObject object_step;

	// output mesh
	static MObject outputMesh;

	static MStatus initialize();
	virtual MStatus compute(const MPlug& plug, MDataBlock& data);
	void createMesh(const MTime& time, const double& stepsize, const double& angledegree, const std::string& grammar, MObject& output);
};


MTypeId LSystemNode::id(0x80000);
MObject LSystemNode::outputMesh;
MObject LSystemNode::time;
MObject LSystemNode::object_degree;
MObject LSystemNode::object_step;
MObject LSystemNode::object_grammar;

/*
MFnNumericAttribute LSystemNode::angle_degree;
MFnNumericAttribute LSystemNode::step_size;
MFnTypedAttribute LSystemNode::grammar_file;
MFnUnitAttribute LSystemNode::input_time;
*/

LSystemNode::LSystemNode()
{}

LSystemNode::~LSystemNode()
{}

MStatus LSystemNode::initialize()
{
	MStatus returnStatus;
	// here I refer the maya tutorial https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__files_Dependency_graph_plugins_The_basics_htm
	MFnUnitAttribute unit_data;
	MFnTypedAttribute typed_data;
	MFnNumericAttribute numeric_data;

	// degree
	LSystemNode::object_degree = numeric_data.create("angle_degree", "ad", MFnNumericData::kDouble, 45.0);

	// step size
	LSystemNode::object_step = numeric_data.create("step_size", "ss", MFnNumericData::kDouble, 1.0);

	// grammar
	LSystemNode::object_grammar = typed_data.create("grammar", "g", MFnData::kString, MFnStringData().create("F \n" "F->F[+F]F[-F]F"));

	// input_time
	LSystemNode::time = unit_data.create("time", "t", MFnUnitAttribute::kTime, 0.0);

	// output mesh
	LSystemNode::outputMesh = typed_data.create("outputMesh", "out", MFnData::kMesh);

	typed_data.setStorable(false);

	returnStatus = addAttribute(LSystemNode::time);
	returnStatus = addAttribute(LSystemNode::outputMesh);
	returnStatus = addAttribute(LSystemNode::object_degree);
	returnStatus = addAttribute(LSystemNode::object_step);
	returnStatus = addAttribute(LSystemNode::object_grammar);

	// input and output
	returnStatus = attributeAffects(LSystemNode::time, LSystemNode::outputMesh);
	return MS::kSuccess;
}

MStatus LSystemNode::compute(const MPlug& plug, MDataBlock& data)
{

	MStatus returnStatus;
	if (plug == outputMesh)
	{
		// get input time
		MDataHandle timeHandle = data.inputValue(time, &returnStatus);
		if (returnStatus != MS::kSuccess) { 
			cerr << "ERROR getting data" << endl; 
		}
		MTime time = timeHandle.asTime();

		// get degree
		MDataHandle degreeHandle = data.inputValue(object_degree, &returnStatus);
		if (returnStatus != MS::kSuccess) {
			cerr << "ERROR getting data" << endl;
		}
		double deg = degreeHandle.asDouble();

		// get step size
		MDataHandle stepHandle = data.inputValue(object_step, &returnStatus);
		if (returnStatus != MS::kSuccess) {
			cerr << "ERROR getting data" << endl;
		}
		double stp = stepHandle.asDouble();

		// get grammar
		MDataHandle grammarHandle = data.inputValue(object_grammar, &returnStatus);
		if (returnStatus != MS::kSuccess) {
			cerr << "ERROR getting data" << endl;
		}
		MString gmr = grammarHandle.asString();

		// get mesh output
		MDataHandle meshHandle = data.outputValue(outputMesh, &returnStatus);
		if (returnStatus != MS::kSuccess) {
			cerr << "ERROR getting data" << endl;
		}

		MFnMeshData meshCreator;
		MObject current = meshCreator.create(&returnStatus);
		if (returnStatus != MS::kSuccess) {
			cerr << "ERROR generate mesh creator" << endl;
		}

		 // transfer from mstring to string
		 string gmr_str = gmr.asChar();
		 createMesh(time, stp, deg, gmr_str, current);
		 if (returnStatus != MS::kSuccess) {
		 	cerr << "ERROR creating mesh" << endl;
		 }

		 meshHandle.set(current);
		 data.setClean(plug);
	}
	return MS::kSuccess;
}

// create mesh here
void LSystemNode::createMesh(const MTime& input, const double& step_size, const double& angle_degree, const std::string& grammar, MObject& outMesh)
{
	lsystem.loadProgramFromString(grammar);
	lsystem.setDefaultAngle(angle_degree);
	lsystem.setDefaultStep(step_size);

	int frame = (int)input.as(MTime::kFilm);
	frame = frame > 0 ? frame : 1;
	std::vector<LSystem::Branch> brches;
	// l-system process
	lsystem.process(frame, brches);
	MPointArray pts;
	// from cylinder.h
	MIntArray faceCounts;
	MIntArray faceConnects;

	// store trees
	// from piazza 
	for (int i = 0; i < brches.size(); i++) {
		MPoint start_point = MPoint(brches[i].first[0], brches[i].first[1], brches[i].first[2]);
		MPoint end = MPoint(brches[i].second[0], brches[i].second[1], brches[i].second[2]);
		CylinderMesh clydm(start_point, end);
		clydm.appendToMesh(pts, faceCounts, faceConnects);
	}
	MFnMesh mmesh;
	mmesh.create(pts.length(), faceCounts.length(), pts, faceCounts, faceConnects, outMesh);
}