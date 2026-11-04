"""Chapter 14: four quick checks for a set of barcode sequences.

1. Ambiguous letters: does any sequence contain letters other than A, C, G, T?
2. Stop codons: does the sequence translate into a protein without internal
   stop codons? (A real protein-coding barcode should.) Use genetic code 2 for
   animal mitochondrial genes such as COI, and 11 for plant chloroplast genes
   such as rbcL and matK.
3. Nearest neighbour: in the alignment, is each sequence's closest relative
   labelled with the same species? If not, the record deserves a closer look.
4. Distance from its own species: is the record, on average (median), more than
   3% different from the other records of its own species? Mislabelled records
   that come in groups pass check 3 (they are each other's nearest neighbours)
   but fail this one.

Usage: python check_records.py aligned.fasta GENETIC_CODE [species_table.tsv]
Example: python check_records.py carps_all.aln.fasta 2 species.tsv

Species names are taken from species_table.tsv (accession <TAB> organism), if
given. NCBI's organism names are standardised, so old synonyms (e.g. "Catla
catla" and "Labeo catla") count as one species. Without a table, the 2nd and
3rd words of each FASTA header are used, which can be misleading.
"""
import statistics
import sys

from Bio import SeqIO
from Bio.Seq import Seq

aln = list(SeqIO.parse(sys.argv[1], "fasta"))
code = int(sys.argv[2])
if len(sys.argv) > 3:
    table = dict(line.rstrip("\n").split("\t")[:2] for line in open(sys.argv[3]) if "\t" in line)
    # Keep genus and species only, so subspecies and varieties count as their species
    species = {acc: " ".join(org.split()[:2]) for acc, org in table.items()}
else:
    species = {r.id: " ".join(r.description.replace("UNVERIFIED: ", "").split()[1:3]) for r in aln}
seqs = {r.id: str(r.seq).upper() for r in aln}


def p_distance(a, b):
    compared = differ = 0
    for x, y in zip(a, b):
        if x != "-" and y != "-":
            compared += 1
            differ += x != y
    return 100 * differ / compared if compared >= 300 else None


def fewest_stops(dna):
    """Smallest number of internal stop codons over the three reading frames."""
    best = None
    for frame in range(3):
        part = dna[frame:]
        part = part[: len(part) - len(part) % 3]
        protein = str(Seq(part).translate(table=code)).rstrip("*")
        stops = protein.count("*")
        best = stops if best is None else min(best, stops)
    return best


problems = 0
print(f"Checking {len(seqs)} sequences (genetic code {code})\n")
for rid, s in seqs.items():
    raw = s.replace("-", "")
    notes = []
    ambiguous = len(raw) - sum(raw.count(b) for b in "ACGT")
    if ambiguous:
        notes.append(f"{ambiguous} ambiguous letters")
    stops = fewest_stops(raw)
    if stops:
        notes.append(f"{stops} internal stop codons")
    neighbours = [(p_distance(s, seqs[o]), o) for o in seqs if o != rid]
    neighbours = [n for n in neighbours if n[0] is not None]
    d, nearest = min(neighbours)
    if species[nearest] != species[rid]:
        notes.append(f"nearest is {nearest} ({species[nearest]}) at {d:.2f}%")
    own = [p_distance(s, seqs[o]) for o in seqs if o != rid and species[o] == species[rid]]
    own = [x for x in own if x is not None]
    if own and statistics.median(own) > 3:
        notes.append(f"median {statistics.median(own):.1f}% from its own species")
    if notes:
        problems += 1
        print(f"{rid:12s} {species[rid]:20s} " + "; ".join(notes))
print(f"\n{problems} of {len(seqs)} records flagged for a closer look.")
