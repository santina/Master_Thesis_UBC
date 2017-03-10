#include <iostream>
#include <fstream>
#include <limits>


bool onEOF(std::ifstream& infile) throw(int) {
	if(infile.eof()){
		return true;
	} else if(infile.fail()){
                std::cerr << "READ_FAILED" << std::endl;
                throw 1;
        } else {
		return false;
	} 
}
void ignoreTillNewLine(std::ifstream& infile){
	const char NEWLINE = '\n';
	infile.ignore(std::numeric_limits<std::streamsize>::max(), NEWLINE);	
}

int main(){
	auto filename = "./testjkh.3col";
	std::ifstream infile(filename);
	int coord;
	double d;
	const char NEWLINE = '\n';
	while(true){
		infile.clear();
		infile >> coord;
		if(onEOF(infile)){
			break;
		}
		else{
			for(int i = 0; i < 2; i ++){
				infile >> d;
				if(onEOF(infile)){
					std::cerr << "UNEXPECTED EOF" << std::endl;
					throw 2;
				}
			}
			ignoreTillNewLine(infile);
			std::cout << coord << std::endl;
		}

	}
}


