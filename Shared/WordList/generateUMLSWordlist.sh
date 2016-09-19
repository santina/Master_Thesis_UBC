#!/bin/bash
set -e
set -x

usage() {
	echo "Usage: `basename $0` UMLSDIR OUTDIR"
	echo ""
	echo "This generates a word-list and associated UMLS CUID list"
	echo "It specifically focuses on semantic types in the following categories:"
	echo "               ANAT/CHEM/DISO/GENE/PHYS"
	echo "It specifically removes the Finding group (T033)."
	echo
	echo " UMLSDIR - Directory containing the various UMLS files"
	echo " OUTDIR - Directory in which to output files"
	echo ""
}
expectedArgs=2

# Show help message if desired
if [[ $1 == "-h" || $1 == '--help' ]]; then
	usage
	exit 0
# Check for expected number of arguments
elif [[ $# -ne $expectedArgs ]]; then
	echo "ERROR: Expecting $expectedArgs arguments"
	usage
	exit 255
fi

# Points towards directory containing UMLS files
umlsDir=$1
outDir=$2

# Download the semantic groups file
wget http://metamap.nlm.nih.gov/Docs/SemGroups_2013.txt

# Extract groups associated with anatomy, chemicals, disorders, genes and phys
grep -P "^ANAT" SemGroups_2013.txt > SemGroups_2013.filtered.txt
grep -P "^CHEM" SemGroups_2013.txt >> SemGroups_2013.filtered.txt
grep -P "^DISO" SemGroups_2013.txt >> SemGroups_2013.filtered.txt
grep -P "^GENE" SemGroups_2013.txt >> SemGroups_2013.filtered.txt
grep -P "^PHYS" SemGroups_2013.txt >> SemGroups_2013.filtered.txt

# Remove the Finding group (T033)
grep -v Finding SemGroups_2013.filtered.txt >> SemGroups_2013.filtered.txt2
mv SemGroups_2013.filtered.txt2 SemGroups_2013.filtered.txt

# Get the type IDs for the groups described above
cut -f 3 -d '|' SemGroups_2013.filtered.txt | sort -u > SemGroups_2013.filtered.ids.txt

#$umlsDir/MRSTY.RRF
#$umlsDir/MRREL.RRF
#$umlsDir/MRCONSO.RRF

semanticTypeIDs=`cat SemGroups_2013.filtered.ids.txt | tr '\n' ',' | sed -e 's/,$//'`
relationshipTypes="has_tradename"

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python=/gsc/software/linux-x86_64/python-2.7.2/bin/python

$python $HERE/helper_generateUMLSWordlist.py --selectedTypeIDs $semanticTypeIDs --selectedRelTypes $relationshipTypes --umlsConceptFile $umlsDir/MRCONSO.RRF --umlsSemanticTypesFile $umlsDir/MRSTY.RRF --umlsRelationshipsFile $umlsDir/MRREL.RRF --outWordlistFile $outDir/umlsWordlist.WithIDs.txt

# To avoid confusion, let's clean up a bit
rm SemGroups_2013.txt
rm SemGroups_2013.filtered.txt
rm SemGroups_2013.filtered.ids.txt

# Sort the umlsWordlist (which will be by the CUIDs in the first column)
sort $outDir/umlsWordlist.WithIDs.txt > $outDir/umlsWordlist.WithIDs.tmp
mv $outDir/umlsWordlist.WithIDs.tmp $outDir/umlsWordlist.WithIDs.txt

# And let's make the raw final word-list by removing CUIDs and SemanticTypeIDs
cut -f 3 -d $'\t' $outDir/umlsWordlist.WithIDs.txt > $outDir/umlsWordlist.Final.txt

# Let's output the NLTK stopwords to a file as well
#python -c "from nltk.corpus import stopwords; print '\n'.join( stopwords.words('english') )" > nltk_stopwords.txt
