"""Appendix H, chart 3: a histogram of the carp barcode distances (Chapter 13).

Every pair of the 28 carp barcodes gives one distance. The histogram counts
how many pairs fall in each 0.5% band, within and between species.

Usage: python chart3_histogram.py carp_pairwise_distances.csv
Output: chart3_histogram.png and .pdf
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
within = [float(r["p_distance_percent"]) for r in rows if r["comparison"] == "within"]
between = [float(r["p_distance_percent"]) for r in rows if r["comparison"] == "between"]
bins = [i * 0.5 for i in range(0, 28)]      # 0, 0.5, 1.0 ... 13.5

fig, ax = plt.subplots(figsize=(5, 3.5), dpi=300)
ax.hist(within, bins=bins, color="#0b0b0b", label=f"Within species ({len(within)} pairs)")
ax.hist(between, bins=bins, facecolor="white", edgecolor="#2a78d6", hatch="////",
        label=f"Between species ({len(between)} pairs)")
ax.set_xlabel("Distance between two barcodes (p-distance, %)")
ax.set_ylabel("Number of pairs")
ax.legend(frameon=False, fontsize=8)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

fig.tight_layout()
fig.savefig("chart3_histogram.png")
fig.savefig("chart3_histogram.pdf")
print(f"Within: max {max(within):.2f}%; between: min {min(between):.2f}%")
