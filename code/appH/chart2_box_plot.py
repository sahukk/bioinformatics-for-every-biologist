"""Appendix H, chart 2: a box plot, with every value shown as a dot.

The same two groups as chart 1. The box shows the middle half of the values,
the line inside it the median, and the whiskers the rest of the range.

Usage: python chart2_box_plot.py ocimum_rbcL_matK_GC.csv
Output: chart2_box_plot.png and .pdf
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
tulsi = [float(r["matK_GC_percent"]) for r in rows if r["species"] == "tenuiflorum"]
other = [float(r["matK_GC_percent"]) for r in rows if r["species"] != "tenuiflorum"]

fig, ax = plt.subplots(figsize=(3.5, 4), dpi=300)
ax.boxplot([tulsi, other], widths=0.5, showfliers=False,
           medianprops=dict(color="#2a78d6", linewidth=2))
# every plant as a dot, spread a little sideways so they do not hide each other
for x, values in ((1, tulsi), (2, other)):
    xs = [x + (i % 5 - 2) * 0.04 for i in range(len(values))]
    ax.scatter(xs, values, s=14, color="#0b0b0b", zorder=3)
ax.set_xticks([1, 2], [f"Tulsi\n(n = {len(tulsi)})", f"Other basils\n(n = {len(other)})"])
ax.set_ylabel("matK GC content (%)")
ax.set_title("matK GC content of each plant", fontsize=9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

fig.tight_layout()
fig.savefig("chart2_box_plot.png")
fig.savefig("chart2_box_plot.pdf")
print("Saved chart2_box_plot.png and .pdf")
