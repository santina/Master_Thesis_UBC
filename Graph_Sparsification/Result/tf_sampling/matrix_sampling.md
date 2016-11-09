# Matrix sampling



## Overview 
Looking at how sampling rate affect the variances of the matrix. 

The idea is that, the same number of singular values produce the same variance in a sampled matrix as the one in the non-sampled matrix. 

There are 10 matrices, each sampled at different rate [0.1 - 0.9] with three replicates [1-3]. So that's a total of 270 sampled matrices. 

## Import data 
Setting up the required packages and import the data 

```r
library(ggplot2)
library(plyr) # note to self: load this before dplyr always. 
library(dplyr)
```

```
## Warning: package 'dplyr' was built under R version 3.2.5
```

```r
library(magrittr)
```


```r
tf <- read.table("termfreq.summary", header=TRUE)
tf_original <- read.table("tf_original.summary", header = TRUE) 
tfidf <- read.table("tfidf.summary", header=TRUE)
tfidf_original <- read.table("tfidf_original.summary", header=TRUE)
```

## Clean up the data a bit

Just setting some column names.

```r
# Let's separate out the replication and rate  in different columns 
tf <- tf %>% tidyr::separate(matrix_name, c("id", "type", "rate", "replicate"), sep = "_") %>% readr::type_convert()
# Fix column name of tfidf and do the same thing 
tfidf$matrix_name <- gsub(".tfidf", "", tfidf$matrix_name)
tfidf$matrix_name <- gsub("tf", "tfidf", tfidf$matrix_name)
tfidf <- tfidf %>% tidyr::separate(matrix_name, c("id", "type", "rate", "replicate"), sep = "_") %>% readr::type_convert()
```

Combine the data.frames 

```r
# Add the original matrix into the tf data.frame 
tf_original$replicate = "1"
tf_original$rate = 1
tf_original <- tf_original %>% tidyr::separate(matrix_name, c("id", "type"), sep = "[.]")
tf <- rbind(tf, tf_original)

# Add the original to the tfidf data.frame 
tfidf_original$replicate = "1"
tfidf_original$rate = 1
tfidf_original <- tfidf_original %>% tidyr::separate(matrix_name, c("id", "type"), sep = "[.]")
tfidf <- rbind(tfidf, tfidf_original)
```
Fix up the types of the columns 

```r
# combine the two
all <- rbind(tf, tfidf)

# Turn nsv into factor 
all$nsv <- as.factor(all$nsv)
all$id <- as.factor(all$id)
all$type <- as.factor(all$type)
```

What the data look like

```r
head(all)
```

```
##   id type rate replicate forbenius maxAcceptableNSV variance nsv
## 1 99   tf  0.7         1    635283              613 335490.4 200
## 2 99   tf  0.7         1    635283              613 419603.2 400
## 3 99   tf  0.7         1    635283              613 466214.0 600
## 4 99   tf  0.7         1    635283              613 495557.8 800
## 5 97   tf  0.3         2    203749              627 101476.5 200
## 6 97   tf  0.3         2    203749              627 129923.9 400
```

```r
str(all)
```

```
## 'data.frame':	2240 obs. of  8 variables:
##  $ id              : Factor w/ 10 levels "9","90","91",..: 10 10 10 10 8 8 8 8 6 6 ...
##  $ type            : Factor w/ 2 levels "tf","tfidf": 1 1 1 1 1 1 1 1 1 1 ...
##  $ rate            : num  0.7 0.7 0.7 0.7 0.3 0.3 0.3 0.3 0.6 0.6 ...
##  $ replicate       : chr  "1" "1" "1" "1" ...
##  $ forbenius       : num  635283 635283 635283 635283 203749 ...
##  $ maxAcceptableNSV: int  613 613 613 613 627 627 627 627 632 632 ...
##  $ variance        : num  335490 419603 466214 495558 101476 ...
##  $ nsv             : Factor w/ 4 levels "200","400","600",..: 1 2 3 4 1 2 3 4 1 2 ...
```

## Analyzing data

For each grouping of id-rate-nsv, calculate the mean variance and the standard devi


```r
tfidf_summary <- all[all$type=="tfidf", ] %>% dplyr::group_by(id, rate, nsv) %>% dplyr::summarise_at(c("variance", "forbenius"), c("mean", "sd")) %>% dplyr::mutate(cov = variance_mean / forbenius_mean)
tf_summary <- all[all$type=="tf", ] %>% dplyr::group_by(id, rate, nsv) %>% dplyr::summarise_at(c("variance", "forbenius"), c("mean", "sd")) %>% dplyr::mutate(cov = variance_mean / forbenius_mean)
```


```r
head(tf_summary)
```

```
## Source: local data frame [6 x 8]
## Groups: id, rate [2]
## 
##       id  rate    nsv variance_mean forbenius_mean variance_sd
##   <fctr> <dbl> <fctr>         <dbl>          <dbl>       <dbl>
## 1      9   0.1    200      22200.37       45839.67    239.8174
## 2      9   0.1    400      28740.32       45839.67    227.9617
## 3      9   0.1    600      32516.21       45839.67    188.0740
## 4      9   0.1    800      34897.89       45839.67    180.0108
## 5      9   0.2    200      54406.88      108437.33    186.6935
## 6      9   0.2    400      69501.83      108437.33    237.3301
## # ... with 2 more variables: forbenius_sd <dbl>, cov <dbl>
```

## Result


```r
# Plot the one for tf 
ggplot(tf_summary, aes(x = rate, y = cov, colour = nsv, group = nsv)) + geom_point() + geom_line() + facet_wrap(~id)
```

![](matrix_sampling_files/figure-html/unnamed-chunk-7-1.png)\
From this plot we can see that lower sampling rate result in smaller coverage, which is measured by taking the ratio of the variance (of given number of singular values) and forbenius norm. The lines are relatively flat and this is consistent across different matrices. This means we could sample the matrix and the same number of singular values would still be representative enough compare to a matrix that's not sampled. 


```r
# Plot tfidf 
ggplot(tfidf_summary, aes(x = rate, y = cov, colour = nsv, group = nsv)) + geom_point() + geom_line() + facet_wrap(~id)
```

![](matrix_sampling_files/figure-html/unnamed-chunk-8-1.png)\

After some thoughts, I realize that sampling the matrix by taking a subset of the word occurences using a probability rate AND THEN convert the result into TFIDF doesn't really make sense. 

TFIDF(occurrences, term) = (1 + log(occurrences)) * log(nDoc/(nDoc with the term))

Just looking at the first term  TF = 1 + log(occurrences).  1+log(x) where x is an integer 1,2,3..., we can calculate that the change of TF is not constant as X increase.  So I'm not sure if sampling occurrences and then converting the result to TFIDF make sense.  

Therefore, I'll try sampling AFTER converting to TFIDF next time. 

From the look of the graph though, the curves are quite flat and sampling seems to be able to give us a good idea of coverage. 

