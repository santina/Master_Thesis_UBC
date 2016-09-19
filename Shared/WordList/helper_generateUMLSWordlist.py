import sys
import argparse
from collections import defaultdict
import string

if __name__ == "__main__":

	# Set up the command line arguments
	parser = argparse.ArgumentParser(description='Generates a fake UMLS data-set and associated word-list')
	parser.add_argument('--selectedTypeIDs', required=True, type=str, help='Comma-delimited list of type IDs that should be included in the word-list')
	parser.add_argument('--selectedRelTypes', required=True, type=str, help='Comma-delimited list of relationship types that should be included in the word-list (e.g. has_tradename)')
	
	parser.add_argument('--umlsConceptFile', required=True, type=argparse.FileType('r'), help='The concept file from the UMLS dataset')
	parser.add_argument('--umlsSemanticTypesFile', required=True, type=argparse.FileType('r'), help='The semantic types file from the UMLS dataset')
	parser.add_argument('--umlsRelationshipsFile', required=True, type=argparse.FileType('r'), help='The relationships file from the UMLS dataset')
	
	parser.add_argument('--outWordlistFile', required=True, type=argparse.FileType('w'), help='Path to output word-list to')
	args = parser.parse_args()
	
	# Get the SemanticTypeIDs and Relationship types that will be filtered for
	selectedTypeIDs = set(args.selectedTypeIDs.split(','))
	selectedRelTypes = set(args.selectedRelTypes.split(','))
	
	filteredConceptIDs = set()
	filteredConceptSemanticTypeIDs = defaultdict(list)
	
	# Get a list of Concept IDs (CUIDs) that are of a semantic type that we want
	print "Filtering CUIDs by semantic type..."
	for line in args.umlsSemanticTypesFile:
		split = line.strip().split('|')
		cuid = split[0]
		semanticTypeID = split[1]
		
		# Filter for the semantic types of interest
		if semanticTypeID in selectedTypeIDs:
			filteredConceptIDs.add(cuid)
			filteredConceptSemanticTypeIDs[cuid].append(semanticTypeID)
			
	# Get the actual terms used for each of the CUIDs that we're interesting in
	print "Extracting terms for filtered CUIDs..."
	filteredConceptsTerms = defaultdict(list)
	for line in args.umlsConceptFile:
		split = line.strip().split('|')
		cuid = split[0]
		language = split[1]
		term = split[14]
		
		# Filter for the concept IDs already discovered
		if cuid in filteredConceptIDs:
			filteredConceptsTerms[cuid].append(term)
	
	# Instantiate a singleton group for every concept ID (so that we can do some grouping)
	groups = { i:[cuid] for i,cuid in enumerate(filteredConceptIDs) }
	lookup = { cuid:i for i,cuid in enumerate(filteredConceptIDs) }
	
	# Search through the relationships and join concepts that have a relationship
	# between them of a type that we want
	print "Grouping CUIDs by relationships..."
	for line in args.umlsRelationshipsFile:
		split = line.strip().split('|')
		cuid1 = split[0]
		cuid2 = split[4]
		relationshipType = split[7]
		
		# Ignore if both CUIDs aren't in our "interesting" list
		if not (cuid1 in filteredConceptIDs and cuid2 in filteredConceptIDs):
			continue
		
		# The relationship is one we care about, so we should put these two concepts into the same groups
		if relationshipType in selectedRelTypes:
			# Get their current groups
			g1,g2 = lookup[cuid1],lookup[cuid2]
			
			# If the groups are different, then we're going to merge them
			if g1 != g2:
				# Merge the contents of the groups
				groups[g1] = list(set(groups[g1]+groups[g2]))
				# Update the lookup table so that all IDs that previously pointed to group2 now point to group1
				for tmpCUID in groups[g2]:
					lookup[tmpCUID] = g1
				# Delete the unneeded group
				del groups[g2]
	
	# Now that we have concepts grouped, we can output the final word-list
	print "Saving grouped CUIDs to word-list..."
	for groupid,groupCUIDs in groups.iteritems():
		
		# Get all the semantic type IDs associated with the list of CUIDs
		semanticTypeIDs = [ semanticTypeID for cuid in groupCUIDs for semanticTypeID in filteredConceptSemanticTypeIDs[cuid] ]
		
		# Get all the terms associated with the list of CUIDs
		terms = [ term for cuid in groupCUIDs for term in filteredConceptsTerms[cuid] ]
			
		# Sort and unique each of the lists
		groupCUIDs = sorted(list(set(groupCUIDs)))
		semanticTypeIDs = sorted(list(set(semanticTypeIDs)))
		terms = sorted(list(set(terms)))
		
		# Output them to the wordlist as a 3 column file (where each column is pipe-delimited)
		line = "%s\t%s\t%s" % ("|".join(groupCUIDs),"|".join(semanticTypeIDs),"|".join(terms))
		args.outWordlistFile.write(line + "\n")
		
