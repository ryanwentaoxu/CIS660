#include "LSystemCmd.h"
#include "LSystem.h"

#include <maya/MGlobal.h>
#include <list>
#include <string>

LSystemCmd::LSystemCmd() : MPxCommand()
{
}

LSystemCmd::~LSystemCmd() 
{
}

MStatus LSystemCmd::doIt( const MArgList& args )
{
	 // message in Maya output window
	 MStatus status;

	 // Add command line arguments
	 MSyntax syntax;
	 status = syntax.addFlag("-s", "-step_size", MSyntax::kDouble);
	 status = syntax.addFlag("-d", "-angle_degree", MSyntax::kDouble);
	 status = syntax.addFlag("-g", "-grammar", MSyntax::kString);
	 status = syntax.addFlag("-n", "-num_iter", MSyntax::kUnsigned);

	 MArgParser argData(syntax, args, &status);
	 double step_size;
	 double angle_degree;
	 MString grammar;
	 int num_iter;
	 if (argData.isFlagSet("-step_size"))
	 {
	 	status = argData.getFlagArgument("-step_size", 0, step_size);
	 }
	 if (argData.isFlagSet("-angle_degree"))
	 {
	 	status = argData.getFlagArgument("-angle_degree", 0, angle_degree);
	 }
	 if (argData.isFlagSet("-grammar"))
	 {
	 	status = argData.getFlagArgument("-grammar", 0, grammar);
	 }
	 if (argData.isFlagSet("-num_iter"))
	 {
	 	status = argData.getFlagArgument("-num_iter", 0, num_iter);
	 }

	 LSystem lsystem;
	 std::vector<LSystem::Branch> brches;
	 lsystem.loadProgramFromString(grammar.asChar());
	 lsystem.setDefaultAngle(angle_degree);
	 lsystem.setDefaultStep(step_size);
	 lsystem.process(num_iter, brches);

	 for (int i = 0; i < brches.size(); i++) {
	 	vec3 start = brches.at(i).first;
	 	vec3 end = brches.at(i).second;
	 	std::string start_x = std::to_string(start[0]);
	 	std::string start_y = std::to_string(start[1]);
	 	std::string start_z = std::to_string(start[2]);
	 	std::string end_x = std::to_string(end[0]);
	 	std::string end_y = std::to_string(end[1]);
	 	std::string end_z = std::to_string(end[2]);

		vec3 normal = (end - start).Normalize();
		std::string normal_x = std::to_string(normal[0]);
		std::string normal_y = std::to_string(normal[1]);
		std::string normal_z = std::to_string(normal[2]);

	 	std::string index =  to_string(i + 1).c_str();
	 	std::string curve_name = "curve_" + index;
	 	std::string nurbscircle_name = "nurbsCircle_" + index;
	 	std::string circle_radius = "0.1";
	 	std::string startPos = "-p " + start_x + " " + start_y + " " + start_z + " ";
	 	std::string endPos = " -p " + end_x + " " + end_y + " " + end_z + " ";

	 	 std::string cmd = "curve -d 1 -p " + start_x + " " + start_y + " " + start_z + " -p " + end_x + " " + end_y + " " + end_z + " -k 0 -k 1 -name " + curve_name + 
			 ";circle -radius " + circle_radius + " -nr " + normal_x + " " + normal_y + " " + normal_z + "-c " + start_x + " " + start_y + " " + start_z + " -name " + nurbscircle_name + 
			 ";select -r " + nurbscircle_name + " " + curve_name + 
			 " ;extrude -ch true -rn false -po 1 -et 2 -rotation 0 -scale 1 -rsp 0 " + "\"" + nurbscircle_name + "\"" +
	 	 	+" " + "\"" + curve_name + "\"" + ";";
	 	char* c = const_cast<char*>(cmd.c_str());
	 	MGlobal::executeCommand(c);
	 }
	 // message in scriptor editor
	 MGlobal::displayInfo("Implement Me!");

     return MStatus::kSuccess;
}

