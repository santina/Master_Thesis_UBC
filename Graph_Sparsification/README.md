#Overview

Graph sparsification is a process of approximating a graph with fewer edges. Sita suggested this approach as one way to decide how many singular values to keep when running SVD on a very large matrix.

Initially, I have been giving the Graphlab program an arbitrary number of singular values, say 1000, to keep whenever I run SVD on a matrix. I then use the forbenius norm and the error estimation to decide how many singular values I want. For example, if the first 300 singular values gives me a forbenius norm of 80% and their error values are small, then can then use the first 300 ranks to proceed to the next step (finding the closest papers for each paper).

That has been a tolerable approach for doing SVD on a matrix with the size of about 1M (number of terms) by 0.2M (number of papers), which takes more than a week on hugin. Since I am about to do SVD on a much larger matrix (1M X 13M), it's important to not just give an arbitrary number of singular values to do unnecessary work and waste time (and electricity).

Sita suggested that I could "sample" the term occurrences in the matrix with a rate (<1), bringing down the sparsity of the matrix and thus speed up the SVD running time. I could then use the result to estimate how many singular values I would need to achieve a satisfiable forbenius norm. I can then use that number to run SVD on the original matrix.

# Experiment setup

The idea is to first test if this idea works at all by experimenting it with a few smaller matrices. Without the proper understanding of linear algebra and thus graph sparsification itself, I need to see if this "hack" works.  

## Data

10 term-frequency files that were created for another experiment. Each has about 12K abstracts.  

## Intermediate files
- Each term-frequency file is sampled at 9 different rate (0.1 ~ 0.9, step = 0.1) and three times for each different rate, creating 10(term-frequency files) X 9 (different rates) X 3 (repetitions) = 270 (matrices)

## Results
- 270 folders, each has the Graphlab output for each matrix


## Resources
- [A course on graph sparsification](https://simons.berkeley.edu/talks/graph-sparsification)
- [PDF slides](http://www.cs.yale.edu/homes/spielman/TALKS/sparseWeiz.pdf)
