# SOPhT
Substitutions On Phylogenetic Three
SOPhT (Substitutions On Phylogenetic Three) ia a simple all-in-one Python 3 sctipt for tracing gene's substitution distribution over a phylogenetic tree. Just launch the script with your Python 3 interpreter of choice and you will pe prompted to enter the names of alignment, tree and output tree files in succession. If all goes well the output file will be a Nexus tree file with gene substitution sount at each node. The label is created from the alignment name, substitution count.
Tips:
1) Try not to overwrite the original file. Just in case.
2) Whitespaces are usually automatically replaced with underscores.
3) Multiple recursive runs with different alignments can be used for multilocus trees.
4) Indel sites are ignored. The script will let you know how many of them your alignment file contains.
5) Try not to use overly complicated sequence names. Symbols like "()", "," or ":" can mess with the parsing blocks.
6) If your Newick tree contains node labels you should tell the script what they are. Otherwise they will be marked as "label" by default, which you can then manually change in the output file.
