"""Reads files; saves as string; splits into <DNA codons; iterates to find match"""

sample = ['GTA','GGG','CAC']

def read_dna(dna_file):
  dna_data = ""
  with open(dna_file ,"r") as f:
    for line in f:
      dna_data += line
  #print dna_data
  return dna_data

def dna_codons(dna):
  codons = []
  for codon in range(0, len(dna), 3):
    if codon + 3 < len(dna):
      codons.append(dna[codon:codon + 3])
  #print codons
  return codons
"""explanation: dna_codons
empty list
for each codon that will be created in a range from 0 to the end of string, in threes,
if this codon + 3 is still short of the end of string, 
append to the list[whole string sliced in [codon to codon + 3, with default 1 count]"""

def match_dna(dna):
  matches = 0
  for codon in dna:
    if codon in sample:
      matches += 1
  return matches

def is_criminal(dna_sample):
  dna_data = read_dna(dna_sample)
  codons = dna_codons(dna_data)
  num_matches = match_dna(codons)
  
  if num_matches >= 3:
    print "%d mathces. Continue investigation." % num_matches
  else:
    print "%d mathces. No enough data to tie." % num_matches
    
is_criminal("suspect1.txt")
is_criminal("suspect2.txt")
is_criminal("suspect3.txt")

      