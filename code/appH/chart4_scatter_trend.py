"""Appendix H, chart 4: a scatter plot with a straight trend line.

Does a longer matK sequence have a different GC content? One dot per basil
plant (Chapter 11 data). The line is the best straight line through the dots;
r tells how closely the dots follow it (from -1 to +1; 0 = no straight-line link).

Usage: python chart4_scatter_trend.py ocimum_rbcL_matK_GC.csv
Output: chart4_scatter_trend.png and .pdf
"""
import csv
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
x = [float(r["matK_length"]) for r in rows]
y = [float(r["matK_GC_percent"]) for r in rows]

slope, intercept = statistics.linear_regression(x, y)
r = statistics.correlation(x, y)

fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=300)
ax.scatter(x, y, s=18, color="#0b0b0b")
xs = [min(x), max(x)]
ax.plot(xs, [slope * v + intercept for v in xs], color="#2a78d6", linewidth=1.5)
ax.set_xlabel("matK sequence length (bases)")
ax.set_ylabel("matK GC content (%)")
ax.set_title(f"{len(x)} basil plants (r = {r:.2f})", fontsize=9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

fig.tight_layout()
fig.savefig("chart4_scatter_trend.png")
fig.savefig("chart4_scatter_trend.pdf")
print(f"r = {r:.2f}; slope = {slope:.3f} percentage points per base")
