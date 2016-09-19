#include <vector>
#include <unordered_map>
#include <memory>


typedef std::vector<std::unique_ptr<std::vector<double>>> VectorizedVectors;
typedef std::vector<std::unique_ptr<const std::vector<double>>> ImmutableVectorizedVectors; 
template <typename KT, typename VT> using MapOfUniqPtrs = std::unordered_map<KT, std::unique_ptr<VT>>;
template <typename T> using UniqPtrToVector = std::unique_ptr<std::vector<T>>;