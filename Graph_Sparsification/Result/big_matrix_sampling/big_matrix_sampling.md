# Big Matrix Sampling 
Santina Lin  
November 26, 2016  

## Overview

This is for examinig the data to prepare for SVD on the big 13-million-abstract matrix. To estimate the number of singular values needed, the following steps were done

- convert the tf to tf-idf 
- scale the tf-idf matrix by 100 
- sample it with a 0.01 sampling rate 
- run SVD on it, specifying nsv = 2000 


```r
library(ggplot2)
library(plyr) # note to self: load this before dplyr always. 
library(dplyr)
```

```
## Warning: package 'dplyr' was built under R version 3.2.5
```

## Data 

We'll look at the log file of the GraphLab output from running collaborative filtering on this matrix. 

```r
singular_value <- read.table("singular_val.summary", header=TRUE)
head(singular_value)
```

```
##   rank singular_value error_estimate
## 1    0        4421.76    2.26297e-04
## 2    1        3828.88    3.51130e-12
## 3    2        2903.89    3.53349e-12
## 4    3        2683.11    3.51741e-12
## 5    4        2652.21    3.66563e-12
## 6    5        2496.15    3.43492e-12
```

### Error estimates 

First let's plot the error 

```r
ggplot(singular_value, aes(x = rank, y = error_estimate)) + geom_point(size=1) + ylab("Error estimate") + xlab("Rank")
```

![](big_matrix_sampling_files/figure-html/error_estimates-1.png)\
It's clear that after some nsv, the error jumps up significantly, so we do not want to use those singular values. Let's find the number of singular values that have less than 0.5 error rate 


```r
nsv <- sum(singular_value$error_estimate < 0.5)
singular_value$error_estimate[nsv]
```

```
## [1] 0.326936
```

```r
singular_value$error_estimate[nsv+1]
```

```
## [1] 1.95962
```

### Singular values 

Plotting the singular value

```r
ggplot(singular_value, aes(x = rank, y = singular_value)) + geom_point(size=1) + ylab("Singular value") + xlab("Rank")
```

![](big_matrix_sampling_files/figure-html/singular_value_plot-1.png)\

As expected in this sanity check, it's a downward curve that drops in tangential slope sharply after the first few singular value. 

### Conclusion

From the error estimation, we'll be using about 973 nsv to run GraphLab on our original big matrix.  


## On the full matrix 

We used GraphLab to estimate 1100 singular values on the full tfidf matrix. 

### Error estimate 

First let's plot the error 

```r
singularval_fullmatrix <- read.table("singularval_fullmatrix.summary", header=TRUE)
ggplot(singularval_fullmatrix, aes(x = rank, y = error_estimate)) + geom_point(size=1) + ylab("Error estimate") + xlab("Rank")
```

![](big_matrix_sampling_files/figure-html/error_estimates_fullmatrix-1.png)\
It's clear that after some nsv, the error jumps up significantly, so we do not want to use those singular values. Let's find the number of singular values that have less than 0.5 error rate 


```r
nsv <- sum(singularval_fullmatrix$error_estimate < 0.5)
singularval_fullmatrix$error_estimate[nsv]
```

```
## [1] 0.305084
```

```r
singularval_fullmatrix$error_estimate[nsv+1]
```

```
## [1] 1.93905
```

### singular values 

```r
ggplot(singularval_fullmatrix, aes(x = rank, y = singular_value)) + geom_point(size=1) + ylab("Singular value") + xlab("Rank")
```

![](big_matrix_sampling_files/figure-html/singular_value_plot_fullmatrix-1.png)\

The number of singular values measured to be useable are 529.
