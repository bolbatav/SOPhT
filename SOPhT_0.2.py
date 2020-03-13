#!/usr/bin/python3
import sys
import argparse

def read_length(raw_tree, sindex, cladel):
 index=sindex+1
 brl=''
 while index<len(raw_tree) and raw_tree[index]!=',' and raw_tree[index]!=')':
  brl+=raw_tree[index]
  index+=1
 raw_tree=raw_tree.replace(cladel+raw_tree[sindex:index], cladel)
 return raw_tree, brl

def tree_file_read(atr):
 with open(atr, 'r') as trf:
  raw_filetext=trf.readlines()
 filetype=''
 if '#NEXUS' in raw_filetext[0]:
  filetype='x'
 elif raw_filetext[0].startswith('(') or raw_filetext[0].startswith('['):
  filetype='w'
 else:
  filetype='e'
 return filetype, raw_filetext

def read_fasta(fasta):
 with open(fasta, 'r') as inf:
  raw_fasta=inf.readlines()
# transfer this block to main function
 if not raw_fasta[0].startswith('>'):
  print('The specified alignment file is not a valid Fasta file.')
  sys.exit()
# The piece below creates the label name from the alignment name. Too many lines of code and too many variables for the task. Guess I'll come back to it later.
 theader=''
 header=''
 for i in fasta:
  if i!='/' and i!='\\':
   theader+=i
  else:
   theader=''
   continue
 for i in theader: 
  if i!='.':
   header+=i
  else:
   break
 del theader
#
 for i in range(len(raw_fasta)):
  raw_fasta[i]=raw_fasta[i].strip()
 alignment={}
 for i in range(len(raw_fasta)):
  if '>' in raw_fasta[i]:
   h=i
   raw_fasta[h]=raw_fasta[h].replace('>', '')
   raw_fasta[h]=raw_fasta[h].replace(' ', '_')
   alignment[raw_fasta[h]]=[]
   continue
  else:
   alignment[raw_fasta[h]]+=[raw_fasta[i].upper()]
   continue
 for i in alignment.keys():
  seq=''
  alignment[i]=seq.join(alignment[i])
 ldel=[]
 deln=0
# this piece deletes indel sites from alignment
 for i in alignment.keys():
  for j in range(len(alignment[i])):
   if (alignment[i])[j]=='-' and j not in ldel:    
    ldel+=[j]
    deln+=1
    continue
   else:
    continue
 ldel=sorted(ldel)
 for i in alignment.keys(): # a crutch, but it works
  tmp=[x for x in alignment[i]]
  for j in ldel[::-1]:
   del tmp[j]
  alignment[i]=''.join(tmp)
 print(deln, 'gap sites found and deleted for', header, 'gene.')
 return alignment, header

def read_newick(raw_tree, taxa=[]):
 raw_tree=''.join(raw_tree)
 raw_tree=raw_tree.replace(' ', '_')
 raw_tree=raw_tree.replace("'", '') # this line is for newick trees generated by Mega; is it worth keeping?
 raw_tree=raw_tree.strip()
 clades={}
 n=0
 clade=''
 cladel=''
 brl=''
 ndl=''
 labels=False
 if '[&r]' in raw_tree.lower():
  root='r'
  raw_tree=raw_tree.replace('[&R]', '')
  raw_tree=raw_tree.replace('[&r]', '')
 elif '[&u]' in raw_tree.lower():
  root='u'
  raw_tree=raw_tree.replace('[&U]', '')
  raw_tree=raw_tree.replace('[&u]', '')
 else:
  root=''
# this piece makes a taxa list for future Nexus file
 if taxa==[]:
  raw_taxa=raw_tree.replace('(', '')
  raw_taxa=raw_taxa.replace(')', '')
  i=0
  taxon=''
  while i<len(raw_taxa):
   while raw_taxa[i]!=':' and raw_taxa[i]!=',' and raw_taxa[i]!='[':
    taxon+=raw_taxa[i]
    i+=1
   taxa+=[taxon]
   taxon=''
   i+=1
   while i<len(raw_taxa) and raw_taxa[i]!=',':
    i+=1
   i+=1
# this piece parses original taxa names into a clade dictionary
 for t in taxa:
  index=raw_tree.find(t)
  sindex=index
  index=index+len(t)
  n+=1
  cladel='<clade_'+str(n)+'>'
  clades[cladel]=['', '', '', '', '', '']
  clades[cladel][0]=t
  if raw_tree[index]=='[':
   index+=1
   if raw_tree[index]=='&':
    index+=1
   while raw_tree[index]!=']':
    ndl+=raw_tree[index]
    index+=1
   index+=1
  if raw_tree[index]==':':
   index+=1
   while index<len(raw_tree) and raw_tree[index]!=',' and raw_tree[index]!=')':
    brl+=raw_tree[index]
    index+=1
  clades[cladel][1]=brl
  clades[cladel][2]=ndl
  raw_tree=raw_tree.replace(raw_tree[sindex:index], cladel)
  brl=''
  ndl=''
#
# collapsing clades
 while '(' in raw_tree:
  i=0 
  while i<len(raw_tree): # do we really need this line?
   if clade.startswith('(') and clade.endswith(')'):
    n+=1
    cladel='<clade_'+str(n)+'>'
    clades[cladel]=['', '', '', '', '', '']
    clades[cladel][0]=clade
    raw_tree=raw_tree.replace(clade, cladel)
    i=i-len(clade)+len(cladel)
    clade=''
    if i<len(raw_tree):
     if raw_tree[i]=='[':
      sindex=i
      i+=1
      if raw_tree[i]=='&':
       i+=1
      while raw_tree[i]!=']':
       ndl+=raw_tree[i]
       i+=1
      clades[cladel][2]=ndl
      raw_tree=raw_tree.replace(cladel+raw_tree[sindex:i+1], cladel)
      i=sindex
      ndl=''
     if i<len(raw_tree) and (raw_tree[i].isalpha() or raw_tree[i].isdigit()):
      labels=True
      sindex=i
      while raw_tree[i]!=':' and raw_tree[i]!=',' and raw_tree[i]!=')':
       ndl+=raw_tree[i]
       i+=1
      clades[cladel][2]=ndl
      raw_tree=raw_tree.replace(cladel+raw_tree[sindex: i], cladel)
      i=sindex
      ndl=''
     if i<len(raw_tree) and raw_tree[i]==':':
      raw_tree, brl = read_length(raw_tree, i, cladel)
      clades[cladel][1]=brl
      brl=''
      continue
     else:
      i+=1
      continue
    else:
     break
   else: 
    if raw_tree[i]=='(':
     clade='('
     i+=1
     continue
    else:
     clade+=raw_tree[i]
     i+=1
     continue
 nat=['', '']
 return clades, labels, taxa, root, nat

def read_nexus(raw_nexus):
 taxa=[]
 tnum=''
 line=''
 raw_tree=''
 clades={}
 n=0
 claden=''
 nat=['', '']
# this piece finds the tree part of Nexus file, builds a taxa list and writes the tree into a separate line
 i=0
# while i<len(raw_nexus):
 while not 'begin trees' in raw_nexus[i].lower():
  nat[0]+=raw_nexus[i]
  i+=1
 while not 'translate' in raw_nexus[i].lower(): 
  nat[0]+=raw_nexus[i]
  i+=1
 nat[0]+=raw_nexus[i]
 i+=1
 while not ((raw_nexus[i].strip()).lower()).startswith('tree'):
  line+=raw_nexus[i].strip()
  nat[0]+=raw_nexus[i]
  i+=1
 l=0
 while l<len(line)-1:
  while l<len(line) and line[l]!=' ':
   l+=1
  l+=1
  while l<len(line)-1 and line[l]!=',':
   tnum+=line[l]
   l+=1
  taxa+=[tnum]
  tnum=''
 if ((raw_nexus[i].strip()).lower()).startswith('tree'): # Don't know why I would want that as a condition. I don't trust programms writing files in such non-standatrized rormat.
  if '[&r]' in raw_nexus[i].lower():
   root='r'
  elif '[&u]' in raw_nexus[i].lower():
   root='u'
  else:
   root=''
  j=0
  while raw_nexus[i][j]!='(':
   j+=1
  while raw_nexus[i][j]!=';':
   raw_tree+=raw_nexus[i][j]
   j+=1
 i+=1
 while i<len(raw_nexus):
  nat[1]+=raw_nexus[i]
  i+=1
# translating Nexus tree into Newick-like one
 i=0
 newick=''
 while i<len(raw_tree):
  tnum=''
  if raw_tree[i]=='[':
   while raw_tree[i]!=']':
    newick+=raw_tree[i]
    i+=1
   newick+=']'
   i+=1
   continue
  elif raw_tree[i]==':':
   while i<len(raw_tree)-1 and raw_tree[i]!=')' and raw_tree[i]!=',':
    newick+=raw_tree[i]
    i+=1
   newick+=raw_tree[i]
   i+=1
   continue
  elif raw_tree[i].isdigit():
   while raw_tree[i]!='[' and raw_tree[i]!=')' and raw_tree[i]!=',':
    tnum+=raw_tree[i]
    i+=1
   newick+=taxa[int(tnum)-1]
   continue
  else:
   newick+=raw_tree[i]
   i+=1
   continue
 newick+=';'
# setting connections to read_newick
 clades, labdel, tdel, rdel, delnat = read_newick(newick, taxa)
 del tdel
 del labdel
 del rdel
 del delnat
# to do: add ignore feature for the second set of square brackets (other node or tip information); the 4'th ([3]) empty line in clades dictionary is reserved for that
 return clades, taxa, root, nat

def subst_count(clades, alignment, header):
 header=header+'_SC='
 for k in clades.keys():
  if header in clades[k][2]:
   print("Your tree file already contains substitution counts for this gene. If you are positive that it doesn't try renaming the alignment file.")
   sys.exit()
 for k in alignment.keys():
  for l in clades.keys():
   if clades[l][0]==k:
    clades[l][4]=list(alignment[k])
 matrix={'o': ['A', 'G', 'T', 'C', 'R', 'Y', 'S', 'W', 'K', 'M', 'B', 'D', 'H', 'V', 'N'],
	'A': ['A', 'R', 'W', 'M', 'A', 'H', 'V', 'A', 'D', 'A', 'N', 'A', 'A', 'A', 'A'],
	'G': ['R', 'G', 'K', 'S', 'G', 'B', 'G', 'D', 'G', 'G', 'G', 'G', 'N', 'G', 'G'],
	'T': ['W', 'K', 'T', 'Y', 'D', 'T', 'B', 'T', 'T', 'H', 'T', 'T', 'T', 'N', 'T'],
	'C': ['M', 'S', 'Y', 'C', 'V', 'C', 'C', 'H', 'B', 'C', 'C', 'N', 'C', 'C', 'C'],
	'R': ['A', 'G', 'D', 'V', 'R', 'N', 'G', 'A', 'G', 'A', 'G', 'R', 'A', 'R', 'R'],
	'Y': ['H', 'B', 'T', 'C', 'N', 'Y', 'C', 'T', 'T', 'C', 'Y', 'T', 'Y', 'C', 'Y'],
	'S': ['V', 'G', 'B', 'C', 'G', 'C', 'S', 'N', 'G', 'C', 'S', 'G', 'C', 'S', 'S'],
	'W': ['A', 'D', 'T', 'H', 'A', 'T', 'N', 'W', 'T', 'A', 'T', 'W', 'W', 'A', 'W'],
	'K': ['D', 'G', 'T', 'B', 'G', 'T', 'G', 'T', 'K', 'N', 'K', 'K', 'T', 'G', 'K'],
	'M': ['A', 'G', 'H', 'C', 'A', 'C', 'C', 'A', 'N', 'M', 'C', 'A', 'M', 'M', 'M'],
	'B': ['N', 'G', 'T', 'C', 'G', 'Y', 'S', 'T', 'K', 'C', 'B', 'K', 'Y', 'S', 'B'],
	'D': ['A', 'G', 'T', 'N', 'R', 'T', 'G', 'W', 'K', 'A', 'K', 'D', 'W', 'R', 'D'],
	'H': ['A', 'N', 'T', 'C', 'A', 'Y', 'C', 'W', 'T', 'M', 'Y', 'W', 'H', 'M', 'H'],
	'V': ['A', 'G', 'N', 'C', 'R', 'C', 'S', 'A', 'G', 'M', 'S', 'R', 'M', 'V', 'V'],
	'N': ['A', 'G', 'T', 'C', 'R', 'Y', 'S', 'W', 'K', 'M', 'B', 'D', 'H', 'V', 'N']}
 uncertainty={'A': 0, 'G': 0, 'T': 0, 'C': 0, 'R': 1, 'Y': 1, 'S': 1, 'W': 1, 'K': 1, 'M': 1, 'B': 2, 'D': 2, 'H': 2, 'V': 2, 'N': 3}
 work_clades=[]
 for k in clades.keys():
  if ',' in clades[k][0]:
   work_clades+=[k]
 for wc in work_clades:
  consensus=[]
  code=[]
  sc=0
  sbr=clades[wc][0].replace('(', '')
  sbr=sbr.replace(')', '')
  sbr=sbr.split(',')
  seq1=clades[sbr[0]][4]
  seq2=clades[sbr[1]][4]
  for i in range(len(seq1)):
   if seq1[i]!=seq2[i]:
    oi=matrix['o'].index(seq1[i]) # Gotta break down what this does. This line is to find what index matches the i'th letter of the seq1 list which is from clades item with the key as the first element of sbr list.
    code=matrix[seq2[i]][oi] # This line searches matrix IUPAC code against the original index (oi) and the i'th letter of the seq2 list which is from clades item with the key as the second element of sbr list.
    if uncertainty[code]>uncertainty[seq1[i]] and uncertainty[code]>uncertainty[seq2[i]]:
     sc+=1
    consensus+=[code]
   else:
    consensus+=[seq1[i]]
  clades[wc][4]=consensus
  clades[wc][5]=str(sc)
  if clades[wc][2]!='':
   clades[wc][2]=clades[wc][2]+','+header+clades[wc][5]
  else:
   clades[wc][2]=header+clades[wc][5]
 for x in clades.keys():
  clades[x][4]=''.join(clades[x][4])
 return clades

def tree_block_gen(clades, root):
 tree='tree TREE1 = '
 if root=='r':
  tree+='[&R] '
 elif root=='u':
  tree+='[&U] '
 klist=[k for k in clades.keys()]
 tree+=str(clades[klist[-1]][0])
 for k in klist[::-1]:
  tree=tree.replace(k, clades[k][0])
  if clades[k][1]!='':
   tree=tree.replace(clades[k][0], (clades[k][0]+':'+clades[k][1]))
  if clades[k][2]!='':
   tree=tree.replace(clades[k][0], (clades[k][0]+'[&'+clades[k][2]+']'))
  if clades[k][0] in taxa:
   index=str(taxa.index(clades[k][0])+1)
   tree=tree.replace(clades[k][0], index)
 if tree[-1]!=';':
  tree+=';'
 return tree

def nexus_gen(taxa, clades, outname, root, nat):
 if nat==['', '']:
  nexus_text='#NEXUS\n\nBegin taxa;\n\tDimensions ntax='+str(len(taxa))+';\n\t\tTaxlabels'
  for i in range(len(taxa)):
   nexus_text+='\n\t\t\t'+taxa[i]+' '
  nexus_text+='\n\t\t\t;\nEnd;'
# left this line to be able to write alignments into the same file; maybe someone needs it; should do the same for nexus though...
  nexus_text+='\nBegin trees;\n\tTranslate'
  for i in range(len(taxa)):
   if i<9:
    nexus_text+='\n\t\t   '+str(i+1)+' '+taxa[i]
   elif i<99:
    nexus_text+='\n\t\t  '+str(i+1)+' '+taxa[i]
   elif i<999:
    nexus_text+='\n\t\t '+str(i+1)+' '+taxa[i]
   else:
    nexus_text+='\n\t\t'+str(i+1)+' '+taxa[i]
   if i<len(taxa)-1:
    nexus_text+=','
  nexus_text+='\n;\n'
  tree=tree_block_gen(clades, root)
  nexus_text=nexus_text+tree+'\nEnd;'
 else:
  tree=tree_block_gen(clades, root)
  nexus_text=nat[0]+tree+'\n'+nat[1]
 f=open(outname, "w")
 f.write(nexus_text)
 f.close()
 return nexus_text

parser=argparse.ArgumentParser(description='SOPhT (Substitutions On Phylogenetic Three) ia an all-in-one Python 3 sctipt for tracing gene\'s substitution distribution over a phylogenetic tree.')
parser.add_argument('-a', '--alignment', type=str, metavar='', required=True, help='Name of the input gene alignment in Fasta format.')
parser.add_argument('-t', '--tree', type=str, metavar='', required=True, help='Name of the input tree file in Newick or Nexus format.')
parser.add_argument('-o', '--out', type=str, metavar='', required=True, help='Name of the output Nexus tree.')
parser.add_argument('-l', '--labels', type=str, metavar='', help='Specify node labels\' names (eg. "bootstrap") if your Newick tree has them. Default = "label".')
arguments=parser.parse_args()

labels=False
alignment, header = read_fasta(arguments.alignment)

filetype, raw_filetext = tree_file_read(arguments.tree)
if filetype=='w':
  clades, labels, taxa, root, nat = read_newick(raw_filetext)
elif filetype=='x':
  clades, taxa, root, nat = read_nexus(raw_filetext)
elif filetype=='e':
  print('The specified tree file is not a valid Newick or Nexus file.')
  sys.exit()

labelname=''
if labels and not arguments.labels:
 print('Label names were not specified and were set to "label". If you would like to specify them re-run the program with --labels argument.')
 labelname='label'
elif labels and arguments.labels:
 labelname=arguments.labels
elif not labels and arguments.labels:
 print('Node labels are not found in your Newick tree. --labels argument ignored.')
 labelname='label'
for i in clades.keys():
 if clades[i][2]!='':
  clades[i][2]=labelname+'='+clades[i][2]

clades=subst_count(clades, alignment, header)
outfile=nexus_gen(taxa, clades, arguments.out, root, nat)

print('Finished!')