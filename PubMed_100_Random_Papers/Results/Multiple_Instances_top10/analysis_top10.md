# Multiple instances considering top 10
Santina Lin  
November 14, 2016  

This shows the result of 92 repeats of [this experiment](result.md). 
The data are split by the type of matrices in order to decrease the time of processing 

# Data preparation and inspection


```r
library(ggplot2)
library(plyr)
library(dplyr)
```

```
## Warning: package 'dplyr' was built under R version 3.2.5
```

```
## 
## Attaching package: 'dplyr'
```

```
## The following objects are masked from 'package:plyr':
## 
##     arrange, count, desc, failwith, id, mutate, rename, summarise,
##     summarize
```

```
## The following objects are masked from 'package:stats':
## 
##     filter, lag
```

```
## The following objects are masked from 'package:base':
## 
##     intersect, setdiff, setequal, union
```

```r
library(knitr) # kable()
```
First load the data 

```r
# A function to prepare the data 
prepare_data <- function(filepath){
  data <- read.table(filepath)  # read in the file 
  colnames(data) <- c("ExperimentNum", "distFunc", "nsv", "precision", "seconds") # Set the column name 
  data$ExperimentNum <- as.factor(data$ExperimentNum) # Make sure experiment numbers are factors
  data 
}

term_frequency <- prepare_data("data/term_freq_precision.result") 
term_binary <- prepare_data("data/term_binary_precision.result")
tf_idf <- prepare_data("data/tfidf_precision.result")
```

Slight inspection of the data 

```r
str(tf_idf)
```

```
## 'data.frame':	5336 obs. of  5 variables:
##  $ ExperimentNum: Factor w/ 92 levels "1","2","3","4",..: 10 10 10 10 10 10 10 10 10 10 ...
##  $ distFunc     : Factor w/ 2 levels "Cosine","Euclidean": 2 1 2 1 2 1 2 1 2 1 ...
##  $ nsv          : int  50 50 100 100 150 150 200 200 250 250 ...
##  $ precision    : num  0.88 0.898 0.916 0.944 0.912 ...
##  $ seconds      : num  48.57 6.97 49.93 7.21 52.54 ...
```

```r
str(term_binary)
```

```
## 'data.frame':	5336 obs. of  5 variables:
##  $ ExperimentNum: Factor w/ 92 levels "1","2","3","4",..: 10 10 10 10 10 10 10 10 10 10 ...
##  $ distFunc     : Factor w/ 2 levels "Cosine","Euclidean": 2 1 2 1 2 1 2 1 2 1 ...
##  $ nsv          : int  50 50 100 100 150 150 200 200 250 250 ...
##  $ precision    : num  0.446 0.487 0.543 0.606 0.594 ...
##  $ seconds      : num  22.72 6.57 24.13 4.18 25.71 ...
```

```r
str(term_frequency)
```

```
## 'data.frame':	5336 obs. of  5 variables:
##  $ ExperimentNum: Factor w/ 92 levels "1","2","3","4",..: 10 10 10 10 10 10 10 10 10 10 ...
##  $ distFunc     : Factor w/ 2 levels "Cosine","Euclidean": 2 1 2 1 2 1 2 1 2 1 ...
##  $ nsv          : int  50 50 100 100 150 150 200 200 250 250 ...
##  $ precision    : num  0.596 0.632 0.695 0.745 0.729 ...
##  $ seconds      : num  46.62 6.21 47.71 6.35 50.34 ...
```

```r
unique(tf_idf$nsv)  # see what are the numbers of singular values that I measured 
```

```
##  [1]   50  100  150  200  250  300  350  400  450  500  550  600  650  700
## [15]  750  800  850  900  950 1000 1050 1100 1150 1200 1250 1300 1350 1400
## [29] 1450
```

As we can see that there are 5336 observations. That's because we have two different distance metrics, 29 different numbers of singular values, and all these are repeated over 92 experiments. This is the same for all three dataset. Each is for a different input matrix into Graphlab. 

Lastly, we'll combine all three dataframes 


```r
tf_idf$matrixType <- factor("TF-IDF")
term_binary$matrixType <- factor("Binary")
term_frequency$matrixType <- factor("Frequency")
all_result <- rbind(tf_idf, term_binary, term_frequency)
str(all_result) # inspect final dataframe
```

```
## 'data.frame':	16008 obs. of  6 variables:
##  $ ExperimentNum: Factor w/ 92 levels "1","2","3","4",..: 10 10 10 10 10 10 10 10 10 10 ...
##  $ distFunc     : Factor w/ 2 levels "Cosine","Euclidean": 2 1 2 1 2 1 2 1 2 1 ...
##  $ nsv          : int  50 50 100 100 150 150 200 200 250 250 ...
##  $ precision    : num  0.88 0.898 0.916 0.944 0.912 ...
##  $ seconds      : num  48.57 6.97 49.93 7.21 52.54 ...
##  $ matrixType   : Factor w/ 3 levels "TF-IDF","Binary",..: 1 1 1 1 1 1 1 1 1 1 ...
```


# Average recalls curves 

The lines are the means of precisions from 92 different experiments for a given singular values. We can see that the performance is fairly consistent across any randomly chosen 100 PMIDs. 


```r
create_curves <- function(data, graphTitle){
  ggplot(data, aes(x=nsv, y=precision, colour=distFunc)) + geom_point(alpha=0.1) + 
  facet_grid(matrixType ~ .) + theme_bw() + ggtitle(graphTitle) + scale_x_continuous(expand = c(0, 0), breaks=seq(0, 1500, by=100)) + 
  labs(x="# singular values",y="Average precision") +
  theme(plot.title = element_text(color="#666666", face="bold", size=16, hjust=0.2, vjust=1))+ 
  stat_summary(fun.y = mean, geom="line", size=1.5)
}
create_curves(all_result, "Average precisions in retrieving related PubMed articles")
```

![](analysis_top10_files/figure-html/unnamed-chunk-5-1.png)\

To see the average maxima for each combinations of parameters: 

```r
# Calculate mean precisions  
all_result_means <- ddply(all_result, c("distFunc", "matrixType", "nsv"), summarise,
      precision = mean(precision), meanTime = mean(seconds))

maxima <- aggregate(precision ~ matrixType + distFunc, max, data=all_result_means)  # see maximum of all combinations 
maxima <- merge(maxima, all_result_means[, c("matrixType", "nsv", "precision")], by=c("matrixType", "precision")) # bring in the number of nsv 
maxima <- arrange(maxima, matrixType, distFunc)[, c(1,3,4,2)] # arrange the dataframe
kable(maxima, format="markdown") # ensure Github can render the table
```



|matrixType |distFunc  |  nsv| precision|
|:----------|:---------|----:|---------:|
|TF-IDF     |Cosine    | 1400| 0.9488416|
|TF-IDF     |Euclidean |  100| 0.9044853|
|Binary     |Cosine    | 1300| 0.8719828|
|Binary     |Euclidean |  300| 0.6278501|
|Frequency  |Cosine    | 1150| 0.8481930|
|Frequency  |Euclidean |  400| 0.7449516|

As demosntrated in the code: I first take the mean of precisions across all samples, for each unique combination of sample number, nsv, distance function, and matrix type. So basically an average for 92 different points. Then I get the maxima prececisions across all number of singular values for each unique combination of distance function and matrixtype. That way we know, on average, at what nsv are the maxima precision is achieved. 

# Distribution of max precision 

Here we take the maxima precision across all number of singular values in each sample. So we should have 92 maxima points for each combination of distance function and matrix type. 


```r
max_mean <- aggregate(precision ~ matrixType + ExperimentNum + distFunc, max, data=all_result)  # see maximum of all combinations 
ggplot(max_mean, aes(x=distFunc, y=precision, fill=distFunc)) + geom_boxplot(show.legend = FALSE) + 
  theme_bw() + facet_wrap(~matrixType) + labs(y="maximum precisions",x="distance function") + 
  theme(legend.title = element_text(size=14), 
        legend.text = element_text(size=14),
        axis.text = element_text(size=12), 
        axis.title = element_text(size=14), 
        strip.text.x = element_text(size=14))
```

![](analysis_top10_files/figure-html/unnamed-chunk-7-1.png)\






```r
# Get standard deviation 
max_mean_sd <- ddply(max_mean, c("matrixType", "distFunc"), summarise,
      avg_max_precision = mean(precision), sd = sd(precision))
kable(max_mean_sd, format="markdown") # ensure Github can render the table
```



|matrixType |distFunc  | avg_max_precision|        sd|
|:----------|:---------|-----------------:|---------:|
|TF-IDF     |Cosine    |         0.9540638| 0.0134976|
|TF-IDF     |Euclidean |         0.9067123| 0.0224186|
|Binary     |Cosine    |         0.8741209| 0.0205064|
|Binary     |Euclidean |         0.6321046| 0.0324885|
|Frequency  |Cosine    |         0.8517526| 0.0241156|
|Frequency  |Euclidean |         0.7514892| 0.0312614|

# Distribution of nsv at maxima precision 

Here we take the nsv at which maxima precision occcurs across all number of singular values in each sample. So we should have 92 nsv points for each combination of distance function and matrix type. 


```r
maxima_nsv <- merge(max_mean, all_result[, c("precision", "nsv")], by="precision") # bring in the number of nsv 
ggplot(maxima_nsv, aes(x=distFunc, y=nsv, fill=distFunc)) + geom_boxplot(show.legend = FALSE) + 
  theme_bw() + facet_wrap(~matrixType) + labs(y="# singular values at maximum precision",x="distance function")+ 
  theme(legend.title = element_text(size=14), 
        legend.text = element_text(size=14),
        axis.text = element_text(size=12), 
        axis.title = element_text(size=14), 
        strip.text.x = element_text(size=14))
```

![](analysis_top10_files/figure-html/unnamed-chunk-10-1.png)\


```r
max_nsv_sd <- ddply(maxima_nsv, c("matrixType", "distFunc"), summarise,
      avg_max_nsv = mean(nsv), sd = sd(nsv))
kable(max_nsv_sd, format="markdown") # ensure Github can render the table
```



|matrixType |distFunc  | avg_max_nsv|       sd|
|:----------|:---------|-----------:|--------:|
|TF-IDF     |Cosine    |    787.3079| 405.8333|
|TF-IDF     |Euclidean |    701.4610| 446.7085|
|Binary     |Cosine    |    820.6219| 404.4732|
|Binary     |Euclidean |    534.4482| 395.5325|
|Frequency  |Cosine    |    791.6722| 380.5501|
|Frequency  |Euclidean |    756.7708| 402.7234|

# Running time

This is to see how long the calculation takes. So it looks like using cosine function is not only more accurate but also takes less time. 


```r
ggplot(all_result_means, aes(x=nsv, y=meanTime, colour=distFunc)) + geom_point() + facet_grid(matrixType ~ .) + 
  theme_bw() + labs(x="number of singular values", y="average time") 
```

![](analysis_top10_files/figure-html/unnamed-chunk-12-1.png)\