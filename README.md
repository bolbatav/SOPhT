# SOPhT
SOPhT (Substitutions On Phylogenetic Three) ia a simple all-in-one Python 3 sctipt for tracing gene's substitution distribution over a phylogenetic tree. Just launch the script with your Python 3 interpreter of choice with arguments pointing towards input files and stating output file name. If all goes well the output file will be a Nexus tree file with gene substitution sount at each node. The label is created from the alignment name, substitution count.
Tips:
1) Try not to overwrite the original file. Just in case.
2) Whitespaces are usually automatically replaced with underscores.
3) Multiple recursive runs with different alignments can be used for multilocus trees.
4) Indel sites are ignored. The script will let you know how many of them your alignment file contains.
5) Try not to use overly complicated sequence names. Symbols like "()", "," or ":" can mess with the parsing blocks.
6) If your Newick tree contains node labels like bootstrap values you should tell the script what they are. Otherwise they will be marked as "label" by default, which you can then manually change in the output file.

# Changes in 0.2:
1) The script no longer works in interactive mode. Instead, it takes arguments like most Linux applications. Use -h to see the options.
2) The script no longer messes up alignment names if there are dots in parent folder names (eg hidden directories).
3) The script now saves the original Nexus file structure.
4) Multiple runs with the same alignment name are now prevented.
