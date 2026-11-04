"""Report the length and GC content of each sequence in a FASTA file.

Usage: python gc_content.py sequences.fasta
"""
import sys

from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

fasta_file = sys.argv[1]

for record in SeqIO.parse(fasta_file, "fasta"):
    length = len(record.seq)
    gc = gc_fraction(record.seq) * 100
    print(f"{record.id}\tlength = {length} bp\tGC = {gc:.2f}%")
