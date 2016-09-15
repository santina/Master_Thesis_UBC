
# Overview
This repository contains the work I have done for my master thesis at University of British Columbia. It's a machine learning project on testing whether SVD could be used to find related articles by using only the keywords inside the abstracts of each article and finding what parameters work the best with SVD.

Here are the basic steps for each different experiment
- Use the downloaded papers from MedLine or PubMed API and extract key biomedical terms
- Create a document-term matrix using an appropriate TF-IDF function
- Perform SVD with GraphLab, with a chosen number of singular values
- Measure row-row distances in the decomposed matrix that represent the document space
- Find the closest rows for the rows corresponding to the target papers
- Compare the predictions with the PubMed database or human annotations (future)

# For reproducibility

## Presentations_Writings

Contains any write-ups, presentations, poster, reports, etc.

## Supplementary_Tools

Contains instructions on obtaining third-party tools and resources (eg. GraphLab, geniatagger, the biomedical phrase list, Medline papers), as well as code written by other lab members.

# Directories for different experiments

These directories contained different experiments. For more information, see the README in these folders.

## TREC2005_Training

Basic experiment on the use of SVD on a small set of abstracts.

## PubMed_100_Random_Papers

Experiment on selecting a set of 100 random PubMed papers and see how well SVD can find their closest papers, evaluated using PubMed's API to search for what PubMed labels as related articles. This experiment was used to choose some initial parameters, such as distance function and term-frequency.

## Shallow_Deep_Neighbors

Experiment on how well SVD can find related articles for each of the 100 random PubMed papers if the dataset contains not just the 100 random papers and their related articles, but also the related articles of the related articles (second level neighbors). To see how well PubMed can be trained with the additional of second level neighbors, the result is compared against another dataset with random papers instead of the second level neighbors.

## TFIDF_Variant_Comparison

Testing different variants of TFIDF on the effect of precision and recalls.

## Distance_Threshold

Testing if cosine distances measured from the decomposed matrices are bimodal and thus allow a cutoff to find related articles.

## Medline_13M

SVD on all the papers available on MedLine (until March 2015), excluding the ones that do not have abstracts.
