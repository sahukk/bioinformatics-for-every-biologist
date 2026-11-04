#!/bin/bash
# Chapter 10: repeat the Chapter 9 analysis on your own laptop.
# Run inside the book's conda environment:  conda activate bioinfo_book

# 1. Make a folder for this analysis and go into it
mkdir -p ch10_is_it_tulsi
cd ch10_is_it_tulsi

# 2. Download the seven basil rbcL sequences from NCBI (Chapter 8)
efetch -db nuccore -format fasta \
  -id MF468180.2,MF468182.1,MF468183.1,MF468186.1,MF468189.1,MF468192.1,MF468195.1 \
  > ocimum_rbcL_7species.fasta

# 3. Check the download: how many sequences, and how long?
grep -c ">" ocimum_rbcL_7species.fasta
seqkit stats ocimum_rbcL_7species.fasta

# 4. Align them with MAFFT
mafft --auto ocimum_rbcL_7species.fasta > ocimum_rbcL_7species.aln.fasta

# 5. Build a tree with IQ-TREE (1000 ultrafast bootstrap replicates)
iqtree -s ocimum_rbcL_7species.aln.fasta -m MFP -B 1000 --seed 12345 --prefix ocimum7

# 6. Look at the result
cat ocimum7.treefile
