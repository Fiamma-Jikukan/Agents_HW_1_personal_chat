"""Draw the Actor-Critic architecture diagram.

Run from the personal_chat folder (matplotlib is only needed here, not by the notebook):
    uv run --no-project --with matplotlib python report/draw_architecture.py report/architecture.png
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

OUT = sys.argv[1]

C = {
    "ink": "#1f2933", "muted": "#52606d",
    "grey": "#e4e7eb", "grey_e": "#9aa5b1",
    "chat": "#e0f2fe", "chat_e": "#0284c7",
    "actor": "#dbeafe", "actor_e": "#2563eb",
    "critic": "#ede9fe", "critic_e": "#7c3aed",
    "eval": "#f3e8ff", "eval_e": "#9333ea",
    "dec": "#fef9c3", "dec_e": "#ca8a04",
    "green": "#15803d", "green_f": "#dcfce7",
    "orange": "#c2410c", "orange_f": "#ffedd5",
    "red": "#b91c1c", "red_f": "#fee2e2",
    "log": "#f1f5f9", "log_e": "#64748b",
}

fig, ax = plt.subplots(figsize=(16, 10), dpi=170)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
fig.patch.set_facecolor("white")


def box(cx, cy, w, h, title, body, face, edge, title_color=None, lw=1.8, title_size=13, body_size=10.5):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=face, ec=edge, lw=lw, zorder=3))
    if body:
        ax.text(cx, cy + h / 2 - 0.3, title, ha="center", va="top", fontsize=title_size, weight="bold",
                color=title_color or edge, zorder=4)
        ax.text(cx, cy - 0.2, body, ha="center", va="center", fontsize=body_size, color=C["ink"],
                zorder=4, linespacing=1.35)
    else:
        ax.text(cx, cy, title, ha="center", va="center", fontsize=title_size, weight="bold",
                color=title_color or edge, zorder=4)


def diamond(cx, cy, w, h, text):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)],
                         closed=True, fc=C["dec"], ec=C["dec_e"], lw=1.8, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=11, weight="bold", color=C["ink"], zorder=4)


def path(points, color, lw=2.0, ls="-", head=True):
    xs, ys = zip(*points)
    ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=color, lw=lw, ls=ls, zorder=2,
            solid_capstyle="butt") if not head else None
    if head:
        for (x0, y0), (x1, y1) in zip(points[:-2], points[1:-1]):
            ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls, zorder=2)
        ax.annotate("", xy=points[-1], xytext=points[-2],
                    arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.35", color=color, lw=lw,
                                    ls=ls, shrinkA=0, shrinkB=0), zorder=2)


def label(x, y, text, color, size=10, weight="normal", ha="center", va="center", bg="white"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color, weight=weight, zorder=5,
            bbox=dict(fc=bg, ec="none", pad=1.5) if bg else None)


# ---------- title ----------
ax.text(0.25, 9.75, "Personal chat - Actor / Critic architecture", fontsize=17, weight="bold", color=C["ink"],
        va="top")
ax.text(0.25, 9.28, "Per user question: at most 3 generation attempts (including the first one)",
        fontsize=11, color=C["muted"], va="top")

# ---------- main row ----------
Y = 6.2
box(1.45, Y, 2.5, 2.1, "Gradio chat", "Hebrew UI\n\nhistory = user messages\n+ final answers only",
    C["chat"], C["chat_e"])
box(4.85, Y, 2.5, 1.7, "ACTOR", "generate_answer()\nwrites a draft answer", C["actor"], C["actor_e"])
box(8.25, Y, 2.5, 1.7, "CRITIC", "evaluate()\nchecks criteria A-D", C["critic"], C["critic_e"])
box(11.55, Y, 2.5, 1.7, "Evaluation", "Pydantic-validated\nis_acceptable: bool\nfeedback: str",
    C["eval"], C["eval_e"])
diamond(14.55, Y, 2.0, 1.45, "is_acceptable?")
diamond(14.55, 3.8, 2.0, 1.45, "attempt < 3?")

# sources
box(6.55, 8.45, 5.0, 0.95, "Background sources: linkedin.txt + summary.txt\n(embedded in both system prompts)", None, C["grey"], C["grey_e"],
    title_color=C["ink"], title_size=11.5)
path([(5.4, 7.97), (5.4, Y + 0.85)], C["grey_e"], lw=1.6, ls=(0, (4, 3)))
path([(7.7, 7.97), (7.7, Y + 0.85)], C["grey_e"], lw=1.6, ls=(0, (4, 3)))

# main flow
path([(2.7, Y), (3.6, Y)], C["ink"])
label(3.15, Y + 0.35, "question\n+ history", C["ink"], size=9.5)
path([(6.1, Y), (7.0, Y)], C["ink"])
label(6.55, Y + 0.33, "draft", C["ink"], size=9.5)
path([(9.5, Y), (10.3, Y)], C["ink"])
label(9.9, Y + 0.33, "JSON", C["ink"], size=9.5)
path([(12.8, Y), (13.55, Y)], C["ink"])

# ---------- exits ----------
# EXIT 1: approved -> back to the chat
path([(14.55, Y + 0.725), (14.55, 7.75), (1.45, 7.75), (1.45, Y + 1.05)], C["green"], lw=2.4)
label(14.85, 7.3, "True", C["green"], size=10.5, weight="bold", ha="left")
label(10.4, 7.75, "  EXIT 1 - approved: answer shown in the chat and added to the history  ",
      C["green"], size=10.5, weight="bold", bg=C["green_f"])

# False -> attempt check
path([(14.55, Y - 0.725), (14.55, 3.8 + 0.725)], C["ink"])
label(14.85, 5.0, "False", C["red"], size=10.5, weight="bold", ha="left")

# FEEDBACK ARC: attempt < 3 -> back to the Actor
path([(13.55, 3.8), (4.85, 3.8), (4.85, Y - 0.85)], C["actor_e"], lw=2.8)
label(13.2, 3.52, "Yes", C["actor_e"], size=10.5, weight="bold")
label(8.9, 4.2, "FEEDBACK ARC: rejected answer + Critic feedback -> Actor writes a revised answer",
      C["actor_e"], size=10.5, weight="bold", bg=C["actor"])

# EXIT 2: attempts exhausted
box(14.55, 1.75, 2.7, 1.3, "EXIT 2 - attempt limit", "notice in the chat;\nrejected drafts only in the log",
    C["orange_f"], C["orange"], title_size=11, body_size=9.5)
path([(14.55, 3.8 - 0.725), (14.55, 1.75 + 0.65)], C["orange"], lw=2.2)
label(14.85, 2.75, "No (3rd rejection)", C["orange"], size=10, weight="bold", ha="left")

# EXIT 3: technical error
box(8.25, 1.75, 4.0, 1.3, "EXIT 3 - technical error", "API call failed / invalid Evaluation output;\n"
    "notice in the chat, reason logged", C["red_f"], C["red"], title_size=11, body_size=9.5)
red_ls = (0, (3, 2.5))
path([(4.2, Y - 0.85), (4.2, 1.75), (6.25, 1.75)], C["red"], lw=1.6, ls=red_ls)
path([(8.25, Y - 0.85), (8.25, 1.75 + 0.65)], C["red"], lw=1.6, ls=red_ls)
path([(11.55, Y - 0.85), (11.55, 1.75), (10.25, 1.75)], C["red"], lw=1.6, ls=red_ls)
label(4.2, 2.9, "error", C["red"], size=9)
label(8.25, 2.9, "error", C["red"], size=9)
label(11.55, 2.9, "invalid", C["red"], size=9)

# ---------- review log ----------
box(8.0, 0.45, 15.5, 0.75, "Review log  (logs/run_log.json)  -  per question: scenario id, question, final status "
    "(approved / max_attempts_reached / technical_error)\nper attempt: attempt number, candidate answer, Critic decision, feedback",
    None, C["log"], C["log_e"], title_color=C["ink"], title_size=10, lw=1.2)

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("saved", OUT)
