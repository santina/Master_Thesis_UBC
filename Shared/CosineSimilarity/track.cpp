#ifndef DEBUGLOG
#define DEBUGLOG 1
#endif

#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <thread>
#include <memory>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <cmath>  

#include "tracking_queue.h"
#include "cpp-utils/Cmn.h"
#include "powergraphload.h"

#include "cxx-prettyprint/prettyprint.hpp"

namespace VOps {
	inline void __dot(const std::vector<double>& v, const std::vector<double>& u, int dim, double& d){
		d = 0;
		for(int k = 0; k < dim; k++){
			d += u[k]*v[k];
		}
	}

	void dot(const ImmutableVectorizedVectors* __byIndex, int start, int end, int threadId, int nTrack, std::string prefix){
		TrackingQueue::MinQueue closest;
		std::ostringstream msgStream, distStream;
		msgStream << "#Thread:" << threadId;
		std::string filename = std::string(prefix) + "." + std::to_string(threadId);
		if(FUtils::exists(filename)){
			msgStream << "..failed:" << filename << " exists";
			Log::Mutexed::cerr(msgStream);	
			return;		
		}
		std::ofstream outfile(filename);
		msgStream << "..tracking:" << filename;
		Log::Mutexed::cerr(msgStream);
		auto& byIndex = *(__byIndex);
		MapOfUniqPtrs<int, std::vector<double>> distances; 
		int dim = byIndex[0]->size();
		int __start = std::max(0, start);
		int __end = std::min((int)byIndex.size(), end); 
		double d = 0;

		for(int i = __start; i < __end; i++){
			outfile << "TRACKING[" << i << "]\t";
			if(DEBUGLOG){
				UniqPtrToVector<double> __distances(new std::vector<double>());
				distances.insert(std::make_pair(i, std::move(__distances)));
			}
			auto& u = *(byIndex[i].get());
			TrackingQueue::fillMinSentinels(closest, nTrack);
			for(int j = 0; j < byIndex.size(); j++){
				auto& v = *(byIndex[j].get());
				VOps::__dot(u, v, dim, d);
				if(DEBUGLOG){ distances[i] -> push_back(d); }
				if(d > closest.top().d){
					TrackingQueue::update(d, j, closest);
				}
			}
			TrackingQueue::dumpf(closest, outfile);
			if(DEBUGLOG){
				distStream << "DEBUG:" << i << "\t" << *(distances[i].get()) << "\t";
				Debug::log(distStream);
				Log::reset(distStream);
			}
		}
		outfile.close();
		msgStream << "..OK:" << filename; 
		Log::Mutexed::cerr(msgStream);
	}

	ImmutableVectorizedVectors intoImmutable(VectorizedVectors& byIndex){
		ImmutableVectorizedVectors __byIndex;
		for(auto& e: byIndex){
			__byIndex.push_back(std::unique_ptr<std::vector<double>>(e.release()));
		}
		byIndex.clear();
		return __byIndex;  
	}

	typedef void (*vectorUpdateF)(std::unique_ptr<std::vector<double>>&); 
	void updateVectorInPlace(vectorUpdateF f, VectorizedVectors& byIndex){
		for(auto &v:byIndex){
			f(v);
		}
		Debug::log(byIndex);
	}
	void normalizeL2(std::unique_ptr<std::vector<double>>& v){
		double norm = 0.0;
		auto __v = v.get();
		for(auto e:*__v){
			norm += e*e;
		}
		norm = std::sqrt(norm);
		for(auto &e:*__v){
			e = e/norm;
		}
	} 
}


int main(int argc, char* argv[]){
	TrackingQueue::SanityCheck::queueOrdering<TrackingQueue::MinTrackingQueueCompare>(true);

	auto binaryname = std::string(argv[0]);

	Cmn::timestamp(binaryname);
	Cmn::Parsed parsed(argc, argv);

	bool debug = parsed.has2("-debug");
	auto prefix = parsed["-prefix"];

	if(parsed.has2("-h")){
		std::cerr << "usage:\n\t./load -nV:3 -eigen-values:./eigenvalues.test -vectors:./vectors.test -dim:3 -track:1 -block-size:2 -prefix:./closest_coords" << std::endl;
		std::exit(1);
	} 

	const int dim = std::stoi(parsed["-dim"]);
	const int track = std::stoi(parsed["-track"]); 
	const int nV = stoi(parsed["-nV"]);
	const int block = stoi(parsed["-block-size"]);


	std::cerr << parsed.json() << std::endl; 

	unsigned int nThreadsSupported = std::thread::hardware_concurrency();
	if(nThreadsSupported == 0){
		std::cerr << "__COULD_NOT_DETECT_HARDWARE_CONCURRENCY__" << std::endl; 
		if(!parsed.has2("-trust-block-size")){
			std::cerr << "..set '-trust-block-size' to ignore" << std::endl;
			std::exit(1);
		}
	} else {
		if(nV / block + 2 > nThreadsSupported){
			std::cerr << "__BLOCK_SIZE_MUST_SATISFY__:nV/BLOCK_SIZE+2<=HARDWARE_CONCURRENCY [" << nThreadsSupported << "]" << std::endl;
			std::exit(1);
		}
	}


	VectorizedVectors byIndex;
	for(int i = 0; i< nV; i++){
		byIndex.push_back(std::unique_ptr<std::vector<double>>(new std::vector<double>()));
	} 
	std::vector<double> eigenValues;

	PowerGraphLoad::loadVectors(parsed["-vectors"], dim, byIndex);
	std::cerr << "#nVectors:" << byIndex.size() << std::endl;
	PowerGraphLoad::loadValues(parsed["-eigen-values"], eigenValues, dim);
	PowerGraphLoad::rescaleVectors(byIndex, eigenValues);
	VOps::updateVectorInPlace(VOps::normalizeL2, byIndex);


	const ImmutableVectorizedVectors iByIndex = VOps::intoImmutable(byIndex);
	const ImmutableVectorizedVectors* __byIndex = &iByIndex;

	std::vector<std::thread> workers;
	for(int b = 0; b < __byIndex->size(); b += block){
		workers.push_back(std::thread(VOps::dot, __byIndex, b, b + block, b/block, track, prefix));
	}
	std::ostringstream msgStream;
	msgStream << "#__DISTRIBUTED_ACROSS_" << workers.size() << "_THREADS__";
	Log::Mutexed::cerr(msgStream);

	for(auto& w : workers){
		w.join();
	}

	
	std::cerr << "#OK" << std::endl;

}



