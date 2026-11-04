"""A NAIVE GC-content script, kept for teaching (Chapter 3, Step B).

It gives wrong answers for lowercase letters and for sequences containing N.
Compare its output with gc_content.py on test_known.fasta.
"""
import sys

name, seq = None, ""
records = []
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith(">"):
        if name:
            records.append((name, seq))
        name, seq = line[1:], ""
    else:
        seq += line
records.append((name, seq))

for name, seq in records:
    gc = (seq.count("G") + seq.count("C")) / len(seq) * 100
    print(f"{name}\tlength = {len(seq)} bp\tGC = {gc:.2f}%")
