#!/bin/bash
# Chapter 13: Can COI barcodes tell India's major carps apart?
# Run inside the book's conda environment:  conda activate bioinfo_book
# Needs barcode_gap.py in the same folder as this script.
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

mkdir -p ch13_carps && cd ch13_carps

# 1. Download the 28 COI barcodes (selection rule: see Chapter 13, Section 3)
efetch -db nuccore -format fasta -id \
EU030668.1,EU030669.1,EU030670.1,EU030671.1,EU030672.1,KX946691.1,KX946693.1,\
KX946601.1,KX946602.1,\
EU417753.1,EU417754.1,EU417755.1,EU417756.1,\
EU417757.1,EU417758.1,EU417759.1,EU417760.1,EU417761.1,KX946686.1,KX946687.1,KX946689.1,\
EU417771.1,EU417772.1,EU417773.1,EU417774.1,EU417775.1,KX946616.1,KX946617.1 \
  > carps_COI.fasta

# 2. Check: 28 sequences, about 650 bases each
grep -c ">" carps_COI.fasta
seqkit stats carps_COI.fasta

# 3. Align
mafft --auto carps_COI.fasta > carps_COI.aln.fasta

# 4. Distances within and between species (the barcode gap)
python "$SCRIPT_DIR/barcode_gap.py" carps_COI.aln.fasta | tee barcode_gap.txt

# 5. Tree with branch support
iqtree -s carps_COI.aln.fasta -m MFP -B 1000 --seed 12345 --prefix carps
