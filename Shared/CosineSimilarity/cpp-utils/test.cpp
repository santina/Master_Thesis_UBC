#include "Cmn.h"

int main(int argc, char* argv[]){
	auto id = std::string(argv[0]);
	Cmn::timestamp(id);
	Cmn::Parsed parsed(argc, argv);
	std::cerr << parsed.json() << std::endl; 
	auto target = std::string(parsed["-infile"]);
	auto lines = FUtils::contents(target);
	std::cerr << Json::json(lines);  
}
