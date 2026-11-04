"""Chapter 11, Step B: a paired dot plot of GC content in rbcL and matK.

Each basil plant appears twice (once per gene), joined by a thin grey line.
A short horizontal bar marks the mean of each gene.

Usage: python plot_gc.py ocimum_rbcL_matK_GC.csv
Output: gc_rbcL_matK.png (for printing) and gc_rbcL_matK.pdf
"""
import csv
import sys
import statistics

import matplotlib
matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt

INK = "#0b0b0b"      # points and text
PAIR_LINE = "#9a9994"  # thin line joining one plant's two values
MEAN = "#2a78d6"     # mean marks (also shown by shape, so grayscale-safe)

rows = list(csv.DictReader(open(sys.argv[1])))
rbcl = [float(r["rbcL_GC_percent"]) for r in rows]
matk = [float(r["matK_GC_percent"]) for r in rows]

fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=300)

# One thin line per plant, joining its rbcL and matK values
for a, b in zip(rbcl, matk):
    ax.plot([0, 1], [a, b], color=PAIR_LINE, linewidth=0.6, zorder=1)

# The individual values, slightly spread sideways so overlapping points show
for x, values in ((0, rbcl), (1, matk)):
    offsets = [x + (i % 5 - 2) * 0.025 for i in range(len(values))]
    ax.scatter(offsets, values, s=18, color=INK, edgecolor="white",
               linewidth=0.5, zorder=2)

# Mean of each gene: a short thick horizontal bar, labelled with its value
for x, values in ((0, rbcl), (1, matk)):
    m = statistics.mean(values)
    ax.plot([x - 0.18, x + 0.18], [m, m], color=MEAN, linewidth=2.5, zorder=1.5)
    ax.annotate(f"mean {m:.1f}%", xy=(x + 0.2, m), va="center",
                fontsize=8, color=INK)

ax.set_xticks([0, 1], ["rbcL", "matK"])
ax.set_xlim(-0.4, 1.6)
ax.set_ylabel("GC content (%)", color=INK)
ax.set_title(f"GC content of two barcode genes\nin {len(rows)} basil plants",
             fontsize=10, color=INK)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.tick_params(colors=INK, labelsize=8)
ax.grid(axis="y", color="#e6e5e0", linewidth=0.5)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("gc_rbcL_matK.png")
fig.savefig("gc_rbcL_matK.pdf")
print("Saved gc_rbcL_matK.png and gc_rbcL_matK.pdf")
