"""Appendix H, chart 1: a bar chart of two group means, with error bars.

Mean matK GC content of tulsi and of the other basils (Chapter 11 data).
Each bar is a mean; the error bar shows one standard deviation either side.

Usage: python chart1_bar_error_bars.py ocimum_rbcL_matK_GC.csv
Output: chart1_bar_error_bars.png and .pdf
"""
import csv
import statistics
import sys

import matplotlib
matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
tulsi = [float(r["matK_GC_percent"]) for r in rows if r["species"] == "tenuiflorum"]
other = [float(r["matK_GC_percent"]) for r in rows if r["species"] != "tenuiflorum"]

labels = [f"Tulsi\n(n = {len(tulsi)})", f"Other basils\n(n = {len(other)})"]
means = [statistics.mean(tulsi), statistics.mean(other)]
sds = [statistics.stdev(tulsi), statistics.stdev(other)]

fig, ax = plt.subplots(figsize=(3.5, 4), dpi=300)
ax.bar(labels, means, yerr=sds, capsize=6, width=0.55,
       color=["#2a78d6", "#d6e6f8"], edgecolor="#0b0b0b", linewidth=0.8)
ax.set_ylim(0, 40)      # a bar chart's axis must start at zero (Section H.6)
ax.set_ylabel("matK GC content (%)")
ax.set_title("Mean matK GC content\n(error bars: 1 standard deviation)", fontsize=9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

fig.tight_layout()
fig.savefig("chart1_bar_error_bars.png")
fig.savefig("chart1_bar_error_bars.pdf")
print(f"Means: tulsi {means[0]:.2f}, other {means[1]:.2f}; SD {sds[0]:.2f}, {sds[1]:.2f}")
