"""Appendix H, chart 5: a line chart of change over time, on a log scale.

The number of bases in GenBank at the end of each year, 1982 to 2026
(table "Growth of GenBank" in the GenBank release notes, release 274.0).
On a log scale, each step up the axis is ten times the one below it.

Usage: python chart5_line_log.py genbank_growth.csv
Output: chart5_line_log.png and .pdf
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
years = [int(r["year"]) for r in rows]
bases = [int(r["base_pairs"]) for r in rows]

fig, ax = plt.subplots(figsize=(5, 3.5), dpi=300)
ax.plot(years, bases, color="#2a78d6", linewidth=1.8, marker="o", markersize=2.5,
        markerfacecolor="#0b0b0b", markeredgewidth=0)
ax.set_yscale("log")
ax.set_xlabel("Year")
ax.set_ylabel("Bases in GenBank (log scale)")
ax.set_title("Growth of GenBank, 1982–2026", fontsize=9)
ax.grid(axis="y", color="#e6e5e0", linewidth=0.5)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

fig.tight_layout()
fig.savefig("chart5_line_log.png")
fig.savefig("chart5_line_log.pdf")
print(f"{years[0]}: {bases[0]:,} bases; {years[-1]}: {bases[-1]:,} bases")
