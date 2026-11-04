"""Appendix H, chart 6: a heatmap of the mean distance between carp species.

Each square is the mean p-distance (%) between the barcodes of two species
(Chapter 13); the diagonal is the distance within a species. Darker = more different.

Usage: python chart6_heatmap.py carp_species_mean_distances.csv
Output: chart6_heatmap.png and .pdf
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.reader(open(sys.argv[1])))
names = rows[0][1:]
values = [[float(v) for v in r[1:]] for r in rows[1:]]

fig, ax = plt.subplots(figsize=(4.8, 4), dpi=300)
im = ax.imshow(values, cmap="Blues", vmin=0)
ax.set_xticks(range(len(names)), names, rotation=30, ha="right")
ax.set_yticks(range(len(names)), names)
# write each value in its square, in white on dark squares
for i, row in enumerate(values):
    for j, v in enumerate(row):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                color="white" if v > 7 else "#0b0b0b")
fig.colorbar(im, ax=ax, label="Mean p-distance (%)", shrink=0.8)
ax.set_title("Mean COI distance between carp species", fontsize=9)

fig.tight_layout()
fig.savefig("chart6_heatmap.png")
fig.savefig("chart6_heatmap.pdf")
print("Saved chart6_heatmap.png and .pdf")
