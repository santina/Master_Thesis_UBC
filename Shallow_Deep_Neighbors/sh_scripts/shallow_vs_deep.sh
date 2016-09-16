## To be run from Feb 10 to Feb 22, hopefully it'll finish by then

## This is for doing term extraction and SVD on shallow vs deep experiment
### Term extraction has been done for the non-random set, but not done for random

### tf-idf form 

# echo "Concatenate with the target and first level neighbors"
# # cat /projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/abstracts_title_termfreq.txt \
# # /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/secondLevel.abstracts.tf > /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.tf
# echo $(date '+%Y %b %d %H:%M') 

# echo "Doing tf-idf calculation"
# python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/tf_idf.py \
# --t /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.tf \
# --tfidf /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.tfidf
# echo $(date '+%Y %b %d %H:%M') 

# echo "Doing format conversion"
# python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/convert_format.py \
# --t /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.tfidf \
# --m /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.matrix
# echo $(date '+%Y %b %d %H:%M') 

# echo "Doing SVD"
# /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/graphlab_command/pubmed_svd.sh \
# /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/term_extracted/target_first_secondLevel.abstracts.matrix \
# 5000 \
# 2833761 \
# /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/Graphlab_output > /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/Graphlab_output/log
# echo $(date '+%Y %b %d %H:%M') 

# echo "non-random set in deep-shallow experiment done"
# echo "Doing term extraction on the random set"
# python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/find_terms.py \
# --f /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/random_abstracts_2821321.txt \
# --out /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/random_abstracts_2821321.tf
# echo $(date '+%Y %b %d %H:%M') 

# echo "Concatenate with the target and first level neighbors"
# cat /projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/abstracts_title_termfreq.txt \
# /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/random_abstracts_2821321.tf > /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.tf
# echo $(date '+%Y %b %d %H:%M') 

# echo "Doing tf-idf"
# python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/tf_idf.py \
# --t /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.tf
# --tfidf /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.tfidf
# echo $(date '+%Y %b %d %H:%M') 

# echo "Doing format  conversion"
# python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/convert_format.py \
# --t /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.tfidf
# --m /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.matrix
# echo $(date '+%Y %b %d %H:%M') 

echo "Doing SVD"
echo $(date '+%Y %b %d %H:%M') 
/projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/graphlab_command/pubmed_svd.sh \
/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/first_second_random_abstracts.matrix \
5000 \
2833761 \
/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/Graphlab_output > /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/Graphlab_output/log
echo $(date '+%Y %b %d %H:%M') 
