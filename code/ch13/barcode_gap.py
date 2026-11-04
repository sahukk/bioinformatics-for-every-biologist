"""Chapter 13: within- and between-species distances (the "barcode gap").

Reads an aligned FASTA file whose headers contain the species name
(as NCBI FASTA headers do, e.g. ">EU030668.1 Labeo rohita voucher ...").
For every pair of sequences it calculates the p-distance: the percentage of
compared positions that differ (positions with a gap in either are skipped).

Usage: python barcode_gap.py aligned.fasta
"""
import itertools
import statistics
import sys

from Bio import SeqIO

records = list(SeqIO.parse(sys.argv[1], "fasta"))
# Species = the 2nd and 3rd words of the header (genus and species)
species = {r.id: " ".join(r.description.split()[1:3]) for r in records}
seqs = {r.id: str(r.seq).upper() for r in records}


def p_distance(a, b):
    compared = differ = 0
    for x, y in zip(a, b):
        if x != "-" and y != "-":
            compared += 1
            differ += x != y
    return 100 * differ / compared


within, between = {}, {}
for a, b in itertools.combinations(seqs, 2):
    d = p_distance(seqs[a], seqs[b])
    if species[a] == species[b]:
        within.setdefault(species[a], []).append(d)
    else:
        pair = tuple(sorted((species[a], species[b])))
        between.setdefault(pair, []).append(d)

print("WITHIN species (p-distance, %)")
for sp in sorted(set(species.values())):
    values = within.get(sp, [0.0])
    n = sum(1 for s in species.values() if s == sp)
    print(f"  {sp:20s} n={n:2d}  mean {statistics.mean(values):5.2f}  max {max(values):5.2f}")

print("BETWEEN species (p-distance, %)")
for pair, values in sorted(between.items()):
    print(f"  {pair[0]:20s} vs {pair[1]:20s}  min {min(values):5.2f}  mean {statistics.mean(values):5.2f}")

max_within = max(max(v) for v in within.values())
min_between = min(min(v) for v in between.values())
print(f"\nLargest within-species distance:  {max_within:.2f}%")
print(f"Smallest between-species distance: {min_between:.2f}%")
print("Barcode gap present" if min_between > max_within else "NO barcode gap: species overlap")
