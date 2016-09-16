MATRIX_TYPES="term_freq tf_idf term_binary"
for MATRIX in $MATRIX_TYPES; do
	for NUM in $(seq 0 9); do
		echo /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/graphlab_command/pubmed_multiple.sh \
			/projects/slin_prj/PubMed_Experiment/random_100_pubmed_repeats/matrices/$MATRIX \
			$NUM \
			1500 \
			/projects/slin_prj/PubMed_Experiment/random_100_pubmed_repeats/GraphLab_Outputs/$MATRIX/
	done
done
