r"""poster/poster.md -> poster/out/poster.pdf (+ PNG preview). Run: python poster/build.py [preview_dpi]

Same idea as a print pipeline: the manuscript is canonical and read-only, every coordinate comes
from SPEC (mm, page origin top-left), and the build ends with machine checks. Looking at the PNG
is still required; the checks only catch what a machine can see.

Look (v3, lab template). Matches the CUPT lab posters for KPS 2026 (J. Jang, poster_refs): navy
header on the lab banner (poster/assets/header_bg.png) with the Sogang IHS shield at the upper right,
three-colour stripe, white page, thin grey-outlined boxes whose heads carry a navy number square
and a navy + orange rule, and an Acknowledgement box with the CUPT logo and the repository QR at
the lower right. Logos sit where the advisor asked (Sogang upper right, CUPT lower right); the
banner, shield and box geometry are taken from the Oct 15 poster PDF.
Text in Source Sans 3 (the lab posters use Arial). A QR code to the repository sits in the
Acknowledgement box (figures/poster/qr_repo.png, made by explore/make_poster_qr.py;
poster/assets/qr_repo.png remains an optional override).
v2 (gray page, shadowed cards, orange number badges, Plex Sans) is in git history (c381842).
Kept from v2:
- text in IBM Plex Sans (poster/fonts, SIL OFL); math in STIX, so a variable is a serif italic
  and is told apart from the sans body at a glance. Plex Sans was the math face too until the
  specimen showed what it costs: it has no \cdot and no \sim, so "h . u_0" and "R ~ 1" were
  silently falling back to DejaVu, and its \int is a text-sized glyph that vanishes in the
  Theta_n equation. Computer Modern ("cm") fixes both but its display integral overshoots the
  line box and collides with the line below, so STIX is the one that fits this layout. Set
  TRATT_MATH=cm|plex|dejavuserif to re-compare. Absolute values are \left|..\right|: a bare
  STIX | is the height of a lowercase l and reads as one;
- bullets are small squares at x-height; the key message is a beige band (as on the ICAMD poster);
- "%%" stat tiles for the few numbers a passer-by should take away.

Manuscript syntax
  front matter: title ("//" = line break), authors, affiliation, contact, footer, session (header corner)
  "## Title"      a panel (numbered automatically); every panel spans the page width
  "@pair"         the next two panels share one band, side by side
  "[[ 0.5 c" ... "|| 0.5" ... "]]"   a row inside a panel: columns with width fractions; "c"
                  centres that column vertically in the row; rows nest
  "> text"        key-message band                        "- text"  bullet
  "![caption](path)" figure, as wide as its column
  "$$ text"       display line: centred, slightly larger, with space around it (equations)
  "=> a // b | c" flow diagram: boxes joined by arrows, a loop arrow back to the first box; "//"
                  splits a box into its symbol line and a smaller description line
  {E12}           notebook entry tag (stripped from print, required on every item)

Checks
1. every paragraph, bullet, band, tile and figure carries an {E..} tag, and each tagged Entry exists
   in notes/lab_notebook.md (nothing goes on the poster without its entry);
2. every figure file exists;
3. the bands fit between the header and the footer (no silent reflow);
4. no text below SPEC["min_pt"].

Layout runs twice inside build(): the first pass measures every band, the second spreads the spare
height evenly between the bands, so the last one ends level with the footer. Panels have no
outline; the number square, the title rule and white space separate them.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
for _f in sorted((ROOT / "poster" / "fonts").glob("*.ttf")):
    font_manager.fontManager.addfont(str(_f))
import os  # noqa: E402

# Text face, both in poster/fonts (SIL OFL). Plex Sans is wider and more open than Source Sans 3;
# TRATT_FONT="Source Sans 3" renders the earlier look for comparison.
FONT = os.environ.get("TRATT_FONT", "IBM Plex Sans")
# Word-by-word placement needs text widths that scale linearly with dpi; hinting breaks that and
# makes long words overrun the next one in a preview rendered at another dpi.
# Math face. IBM Plex Sans has no \cdot and no \sim, so a custom all-Plex fontset silently
# falls back to DejaVu for "h . u_0" and "R ~ 1"; its \int is also a text-sized glyph, which
# the Theta_n equation needs to be bigger than. Set TRATT_MATH to compare.
MATH = os.environ.get("TRATT_MATH", "stix")
_math = ({"mathtext.fontset": "custom", "mathtext.rm": FONT, "mathtext.it": f"{FONT}:italic",
          "mathtext.bf": f"{FONT}:bold", "mathtext.sf": FONT}
         if MATH == "plex" else {"mathtext.fontset": MATH})
matplotlib.rcParams.update({"text.hinting": "none", "text.hinting_factor": 1, "font.family": FONT,
                            "pdf.fonttype": 42,   # TrueType in the PDF: editable, accepted by print shops
                            **_math})
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

MS = ROOT / "poster" / "poster.md"
OUT = ROOT / "poster" / "out"
ASSETS = ROOT / "poster" / "assets"
NOTEBOOK = ROOT / "notes" / "lab_notebook.md"

# A0 portrait, same as the ICAMD 2025 poster (841 x 1189 mm). Check the KPS rule before printing.
SPEC = dict(
    W=841, H=1189, margin=16, gap=14, cols=2, pad=11,
    header_h=110, stripe_h=5, footer_h=53,
    title_pt=52, authors_pt=30, head_pt=40, badge_pt=30, body_pt=28, callout_pt=29, caption_pt=23,
    stat_pt=36, stat_label_pt=23, eq_pt=30, min_pt=23,
    leading=1.3, para_gap=6, side_text=0.64, panel_gap=8, fig_gap=4,
    navy="#0f2a3a", accent="#e8743b", page="#ffffff", card="#ffffff", edge="#7d868f", key="#fbf1d9",
    ink="#111111", ink2="#3f4852", tint="#f4f6f7",
    stripe=("#3a3a3a", "#e04b3a", "#f08a3c"),
)
PT_MM = 25.4 / 72
XH = {"IBM Plex Sans": 0.516}.get(FONT, 0.49)   # x-height / em (Source Sans 3: 0.49)


# ───────────── manuscript ─────────────

TAG = re.compile(r"\{E(\d+)\}")


def parse(text):
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    panels, cur, pending, stack, group = [], None, 0, [], 0

    def add(item):
        (stack[-1]["cols"][-1]["items"] if stack else cur["items"]).append(item)

    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if block == "@pair":
            pending, group = 2, group + 1
            continue
        if block.startswith("## "):
            cur = dict(title=block[3:].strip(), items=[], group=group if pending else None)
            pending = max(0, pending - 1)
            panels.append(cur)
            continue
        if block.startswith("[["):
            w, *opt = block[2:].split()
            row = dict(kind="row", cols=[dict(w=float(w), center="c" in opt, items=[])], tags=None)
            add(row)
            stack.append(row)
            continue
        if block.startswith("||"):
            w, *opt = block[2:].split()
            stack[-1]["cols"].append(dict(w=float(w), center="c" in opt, items=[]))
            continue
        if block == "]]":
            stack.pop()
            continue
        m = re.match(r"!\[(.*?)\]\((.*?)\)(.*)", block, re.S)
        if m:
            add(dict(kind="fig", caption=m[1], path=m[2], tags=TAG.findall(m[3])))
            continue
        if block.startswith("- "):
            for b in re.split(r"\n- ", block[2:]):
                b = " ".join(b.split())
                add(dict(kind="bullet", text=TAG.sub("", b).strip(), tags=TAG.findall(b)))
            continue
        if block.startswith("=>"):
            t = " ".join(block[2:].split())
            add(dict(kind="flow", boxes=[b.strip() for b in TAG.sub("", t).split("|")], tags=TAG.findall(t)))
            continue
        if block.startswith("$$"):
            t = " ".join(block[2:].split())
            add(dict(kind="eq", text=TAG.sub("", t).strip(), tags=TAG.findall(t)))
            continue
        kind = "callout" if block.startswith(">") else "para"
        t = " ".join(re.sub(r"^>\s?", "", block, flags=re.M).split())
        add(dict(kind=kind, text=TAG.sub("", t).strip(), tags=TAG.findall(t)))
    return meta, panels


# ───────────── typesetting ─────────────

TOKEN = re.compile(r"\$[^$]+\$|\*\*[^*]+\*\*|[^\s$*]+|\*")   # a lone * (corresponding author) is a word


class Page:
    def __init__(self):
        s = SPEC
        self.fig = plt.figure(figsize=(s["W"] / 25.4, s["H"] / 25.4), dpi=100)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, s["W"])
        self.ax.set_ylim(s["H"], 0)
        self.ax.axis("off")
        self.r = self.fig.canvas.get_renderer()
        self._w = {}

    def width(self, tok, pt, weight="normal"):
        key = (tok, pt, weight)
        if key not in self._w:
            t = self.ax.text(0, 0, tok, fontsize=pt, fontweight=weight, family=FONT)
            self._w[key] = t.get_window_extent(self.r).width / self.fig.dpi * 25.4
            t.remove()
        return self._w[key]

    def flow(self, text, x, y, w, pt, color=None, weight="normal", indent=0.0, align="left", z=3, draw=True,
             strong=None):
        """Word-by-word placement with wrapping; $..$ and **..** stay atomic, **..** is semibold (in colour
        `strong` if given). Returns the y (mm) just below the last line."""
        color = color or SPEC["ink"]
        lh = pt * PT_MM * SPEC["leading"]
        sp = self.width("a a", pt) - 2 * self.width("a", pt)
        y = y + pt * PT_MM                                  # baseline of the first line
        toks, prev = [], 0
        for m in TOKEN.finditer(text):
            glue = m.start() == prev and bool(toks)
            prev = m.end()
            s, wgt, col = m[0], weight, color
            if s.startswith("**"):
                s, wgt, col = s[2:-2], "semibold", strong or color
            toks.append((s, wgt, col, glue))
        lines, line, lw = [], [], 0.0
        for s, wgt, col, g in toks:
            tw = self.width(s, pt, wgt)
            add = tw + (0 if g or not line else sp)
            if line and lw + add > w - indent:
                k = len(line)                                # a glued run ending the line moves along
                while g and k > 1 and line[k - 1][3]:
                    k -= 1
                if g:
                    k -= 1
                carry = line[k:] if k > 0 else []
                kept = line[:k] if k > 0 else line
                lines.append((kept, sum(t[4] for t in kept) + sp * sum(1 for t in kept[1:] if not t[3])))
                line = [(cs, cw, cc, i > 0 and cg, ctw) for i, (cs, cw, cc, cg, ctw) in enumerate(carry)]
                lw = sum(t[4] for t in line) + sp * sum(1 for t in line[1:] if not t[3])
                add = tw if not line else tw + (0 if g else sp)
            line.append((s, wgt, col, g if line else False, tw))
            lw += add
        if line:
            lines.append((line, lw))
        for line, lw in lines:
            cx = x + indent + ((w - indent - lw) / 2 if align == "center" else 0)
            first = True
            for s, wgt, col, g, tw in line:
                if not g and not first:
                    cx += sp
                if draw:
                    self.ax.text(cx, y, s, fontsize=pt, color=col, family=FONT, zorder=z, fontweight=wgt,
                                 va="baseline")
                cx += tw
                first = False
            y += lh
        return y - lh + pt * PT_MM * 0.35 if lines else y - pt * PT_MM

    def image(self, path, x, y, w, h=None, z=2):
        """Place an image at (x, y) mm, width w; height from the aspect ratio unless given."""
        img = mpimg.imread(path)
        h = h or w * img.shape[0] / img.shape[1]
        a = self.fig.add_axes([x / SPEC["W"], 1 - (y + h) / SPEC["H"], w / SPEC["W"], h / SPEC["H"]], zorder=z)
        a.imshow(img, cmap="gray", interpolation="lanczos")
        a.axis("off")
        return h

    def box(self, x, y, w, h, fc, r=2.5, z=1, ec="none", lw=0.0):
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                         fc=fc, ec=ec, lw=lw, zorder=z))


# ───────────── items ─────────────

def bullet(P, it, x, y, w, draw=True):
    s = SPEC
    if draw:
        d = s["body_pt"] * PT_MM * 0.24                     # marker side
        mid = y + s["body_pt"] * PT_MM * (1 - XH / 2)       # middle of the x-height of the first line
        P.box(x + 0.5, mid - d / 2, d, d, s["ink"], r=0, z=3)
    return P.flow(it["text"], x, y, w, s["body_pt"], indent=7, draw=draw,
                  strong=s["navy"]) + s["para_gap"]


def callout(P, it, x, y, w, draw=True):
    s = SPEC
    y1 = P.flow(it["text"], x + 10, y + 9, w - 20, s["callout_pt"], s["ink"], draw=draw, strong=s["accent"]) + 8
    if draw:
        P.box(x, y, w, y1 - y, s["key"], r=0, z=2)
        P.box(x, y, 2.4, y1 - y, s["accent"], r=0, z=2)
    return y1 + s["para_gap"]


def stats(P, it, x, y, w, draw=True):
    s = SPEC
    n = len(it["tiles"])
    g = 6
    tw = (w - (n - 1) * g) / n
    vh = s["stat_pt"] * PT_MM * 1.05
    bottoms = []
    for i, t in enumerate(it["tiles"]):
        tx = x + i * (tw + g)
        if draw:
            P.flow(t["value"], tx, y + 3, tw, s["stat_pt"], s["accent"], weight="semibold", align="center")
        bottoms.append(P.flow(t["label"], tx + 4, y + 3 + vh + 1, tw - 8, s["stat_label_pt"], s["ink2"],
                              align="center", draw=draw))
    y1 = max(bottoms) + 4
    if draw:
        for i in range(n):
            P.box(x + i * (tw + g), y, tw, y1 - y, s["tint"], r=0, z=2)
    return y1 + s["para_gap"]


def equation(P, it, x, y, w, draw=True):
    s = SPEC
    return P.flow(it["text"], x, y + 1, w, s["eq_pt"], align="center", draw=draw) + s["para_gap"] + 1.5


def flow_diagram(P, it, x, y, w, draw=True):
    """Boxes left to right joined by arrows, with a return arrow underneath (one loop per time step).
    A box "symbol // description" sets the symbol large and the description small below it."""
    s = SPEC
    n, aw = len(it["boxes"]), 12.0
    bw = (w - (n - 1) * aw) / n
    parts = [[t.strip() for t in b.split("//")] for b in it["boxes"]]

    def block(ps, bx, by, draw):
        yy = P.flow(ps[0], bx + 3, by, bw - 6, s["eq_pt"] - 2, align="center", draw=draw)
        for t in ps[1:]:
            yy = P.flow(t, bx + 3, yy + 1.5, bw - 6, s["caption_pt"], s["ink2"], align="center", draw=draw)
        return yy - by

    h = max(block(ps, 0, 0, False) for ps in parts) + 6
    if draw:
        for i, ps in enumerate(parts):
            bx = x + i * (bw + aw)
            P.box(bx, y, bw, h, s["key"], r=0, z=2)
            P.box(bx, y, bw, 1.4, s["accent"], r=0, z=2)
            block(ps, bx, y + (h - block(ps, 0, 0, False)) / 2, True)
            if i < n - 1:
                P.ax.annotate("", xy=(bx + bw + aw - 0.8, y + h / 2), xytext=(bx + bw + 0.8, y + h / 2),
                              arrowprops=dict(arrowstyle="-|>", color=s["accent"], lw=2.6, mutation_scale=20),
                              zorder=3)
        ly = y + h + 5                                      # loop: next time step
        P.ax.plot([x + w - bw / 2, x + w - bw / 2, x + bw / 2], [y + h, ly, ly], color=s["ink2"], lw=1.8,
                  zorder=3)
        P.ax.annotate("", xy=(x + bw / 2, y + h + 0.3), xytext=(x + bw / 2, ly),
                      arrowprops=dict(arrowstyle="-|>", color=s["ink2"], lw=1.8, mutation_scale=16), zorder=3)
        P.ax.text(x + w / 2, ly, r"next time step $\tilde t$", fontsize=s["caption_pt"], color=s["ink2"],
                  family=FONT, ha="center", va="center", zorder=4,
                  bbox=dict(facecolor="white", edgecolor="none", pad=2))
    return y + h + 5 + 4 + s["para_gap"]


def aspect(path):
    a = mpimg.imread(path)
    return a.shape[0] / a.shape[1]


def items(P, its, x, y, w, draw, check):
    """Lay out a list of items in the column (x, w) from y down; returns the y below the last one.
    With draw=False nothing is drawn, so the same call measures. check(it) records tag problems."""
    s = SPEC
    for it in its:
        if draw:
            check(it)
        k = it["kind"]
        if k == "row":
            gap, xs, ws = s["gap"], [], []
            avail = w - gap * (len(it["cols"]) - 1)
            cx = x
            for c in it["cols"]:
                xs.append(cx)
                ws.append(avail * c["w"])
                cx += avail * c["w"] + gap
            hs = [items(P, c["items"], cx_, 0.0, w_, False, check) for c, cx_, w_ in zip(it["cols"], xs, ws)]
            rh = max(hs)
            if draw:
                for c, cx_, w_, h_ in zip(it["cols"], xs, ws, hs):
                    items(P, c["items"], cx_, y + ((rh - h_) / 2 if c["center"] else 0.0), w_, True, check)
            y += rh
        elif k == "fig":
            f = ROOT / it["path"]
            if it["path"] == "none":                        # "![text](none)": a caption-size note
                y = P.flow(it["caption"], x, y, w, s["caption_pt"], s["ink2"], draw=draw) + s["para_gap"]
                continue
            if not f.exists():
                continue
            h = w * aspect(f)
            if draw:
                P.image(f, x, y, w, h=h)
            y += h + s["fig_gap"]
            if it["caption"]:
                y = P.flow(it["caption"], x, y, w, s["caption_pt"], s["ink2"], draw=draw)
            y += s["para_gap"]
        elif k == "bullet":
            y = bullet(P, it, x, y, w, draw)
        elif k == "callout":
            y = callout(P, it, x, y, w, draw)
        elif k == "eq":
            y = equation(P, it, x, y, w, draw)
        elif k == "flow":
            y = flow_diagram(P, it, x, y, w, draw)
        else:
            y = P.flow(it["text"], x, y, w, s["body_pt"], draw=draw, strong=s["navy"]) + s["para_gap"]
    return y


HEAD = 32.0     # number square, title and rule


def head(P, num, title, x, y0, w):
    s = SPEC
    sq = 12.1
    P.box(x, y0 + 4, sq, sq, s["navy"], r=0, z=3)
    P.ax.text(x + sq / 2, y0 + 4 + sq / 2, str(num), fontsize=23.2, color="white", family=FONT,
              fontweight="bold", ha="center", va="center", zorder=4)
    P.flow(title, x + sq + 4.5, y0 + 0.5, w - sq - 4.5, s["head_pt"], s["ink"], weight="semibold")
    P.box(x, y0 + 24, w * 0.86, 0.7, s["navy"], r=0, z=3)
    P.box(x + w * 0.875, y0 + 24, w * 0.125, 0.7, s["accent"], r=0, z=3)


def fit(P, path, x, y, w, h, align="right"):
    """Largest copy of an image inside the box (x, y, w, h), centred vertically; returns its width."""
    img = mpimg.imread(path)
    a = img.shape[0] / img.shape[1]
    iw = min(w, h / a)
    P.image(path, x + (w - iw if align == "right" else 0), y + (h - iw * a) / 2, iw, h=iw * a)
    return iw


# ───────────── page ─────────────

def build(preview_dpi=60):
    s = SPEC
    meta, panels = parse(MS.read_text(encoding="utf8"))
    known = set(re.findall(r"^## .*?Entry (\d+)\b", NOTEBOOK.read_text(encoding="utf8"), flags=re.M))
    problems, used = [], set()
    P = Page()
    ax = P.ax
    W, H, M = s["W"], s["H"], s["margin"]

    # page, header, stripe
    ax.add_patch(plt.Rectangle((0, 0), W, H, color=s["page"], lw=0, zorder=0))
    ax.add_patch(plt.Rectangle((0, 0), W, s["header_h"], color=s["navy"], lw=0, zorder=1))
    if (ASSETS / "header_bg.png").exists():             # in the page axes, under the title text
        bg = mpimg.imread(ASSETS / "header_bg.png")          # drawn for 130 mm; trim rows, never stretch
        keep = min(bg.shape[0], round(bg.shape[0] * s["header_h"] / 130))
        top = (bg.shape[0] - keep) // 2
        ax.imshow(bg[top:top + keep], extent=(0, W, s["header_h"], 0), aspect="auto",
                  zorder=1.5, interpolation="lanczos")
        ax.set_xlim(0, W)
        ax.set_ylim(H, 0)
    seg = (0.0, 0.58, 0.60, 0.84, 0.86, 1.0)
    for i, c in enumerate(s["stripe"]):
        ax.add_patch(plt.Rectangle((seg[2 * i] * W, s["header_h"] + 2), (seg[2 * i + 1] - seg[2 * i]) * W,
                                   s["stripe_h"], color=c, lw=0, zorder=1))
    logo_w = 0
    if (ASSETS / "logo_ihs.png").exists():                  # same size and inset as on the Oct 15 poster, mirrored
        logo_w = 100
        P.image(ASSETS / "logo_ihs.png", W - 22.4 - 55.4, (s["header_h"] - 79.7) / 2, 55.4, h=79.7)
    if meta.get("session"):                                 # kept out of the way, in the empty left corner
        P.flow(meta["session"], M + 6, 14, 150, s["caption_pt"], "#9fb3c2")
    tw = W - 2 * M - 2 * logo_w
    y = 15 - s["title_pt"] * PT_MM * (s["leading"] - 1)
    for line in meta.get("title", "").split("//"):           # "//" in the title = manual line break
        y = P.flow(line.strip(), M + logo_w, y + s["title_pt"] * PT_MM * (s["leading"] - 1), tw, s["title_pt"],
                   "white", weight="semibold", align="center") - s["title_pt"] * PT_MM * 0.35
    y = P.flow(meta.get("authors", ""), M + logo_w, y + 13, tw, s["authors_pt"], "white", align="center")
    P.flow(meta.get("affiliation", ""), M + logo_w, y + 4, tw, s["authors_pt"] - 8, "#c9d6e0", align="center")

    # Footer: stable zones for the grant, CUPT mark, and repository QR.
    fy = H - s["footer_h"]
    ax.plot([M, W - M], [fy - 1.4, fy - 1.4], color=s["edge"], lw=0.9, zorder=2)
    left = M + s["pad"]
    title_baseline = fy + 17.5
    sq = 6.7
    P.box(left, title_baseline - sq + 0.4, sq, sq, s["navy"], r=0, z=3)
    ax.text(left + sq + 3.2, title_baseline, "Acknowledgement", fontsize=s["head_pt"] - 6,
            color=s["ink"], family=FONT, fontweight="semibold", va="baseline", zorder=3)

    qr = ASSETS / "qr_repo.png"
    if not qr.exists():
        qr = ROOT / "figures" / "poster" / "qr_repo.png"
    qr_w = min(37.0, s["footer_h"] - 12.0)
    qr_x = W - M - qr_w - 1.5
    qr_y = fy + (s["footer_h"] - qr_w) / 2
    if qr.exists():
        P.image(qr, qr_x, qr_y, qr_w, h=qr_w)
    else:
        problems.append("missing footer QR")
    # QR destination is the project repository; remove the awkward side caption.
    # Keep the logo and QR as a restrained, aligned footer group.
    cupt_right = qr_x - 16.0
    cupt_left = cupt_right - 115.0
    cupt = ASSETS / "logo_cupt.png"
    if cupt.exists():
        fit(P, cupt, cupt_left, fy + 7, 115.0, s["footer_h"] - 14, align="right")
    else:
        problems.append("missing CUPT footer logo")
    acknowledgements = " · ".join(v for k, v in meta.items() if k in ("footer", "contact"))
    grant_width = cupt_left - left - 22
    P.flow(acknowledgements, left, fy + 23.0, grant_width, s["caption_pt"] + 2, s["ink"])

    def check(it):
        if it["tags"] is None:                              # rows carry no tag; their items do
            return
        if not it["tags"]:
            problems.append(f"untagged {it['kind']}: {it.get('text', it.get('caption', ''))[:50]!r}")
        for t in it["tags"]:
            used.add(int(t))
            if t not in known:
                problems.append(f"tag E{t} is not an Entry in the notebook")
        if it["kind"] == "fig" and it["path"] != "none" and not (ROOT / it["path"]).exists():
            problems.append(f"missing figure {it['path']}")

    bands = []
    for p in panels:
        if p["group"] is not None and bands and bands[-1][0]["group"] == p["group"]:
            bands[-1].append(p)
        else:
            bands.append([p])
    top = s["header_h"] + s["stripe_h"] + 2 + s["panel_gap"] + 4
    bottom = fy - 6
    full = W - 2 * M

    def band(b, y0, draw):
        n = len(b)
        pw = (full - (n - 1) * 2 * s["gap"]) / n
        ends = []
        for k, p in enumerate(b):
            x = M + s["pad"] + k * (pw + 2 * s["gap"])
            w = pw - 2 * s["pad"]
            if draw:
                head(P, number[id(p)], p["title"], x, y0, w)
            ends.append(items(P, p["items"], x, y0 + HEAD, w, draw, check))
        if draw and n == 2:                                 # hairline between the two panels of a band
            mid = M + pw + s["gap"]
            ax.plot([mid, mid], [y0 + 2, max(ends) - s["para_gap"]], color=s["edge"], lw=0.8, zorder=2)
        return max(ends) - s["para_gap"]

    number = {id(p): k + 1 for k, p in enumerate(panels)}
    heights = [band(b, 0.0, False) for b in bands]
    spare = bottom - top - sum(heights) - s["panel_gap"] * (len(bands) - 1)
    gap = s["panel_gap"] + max(0.0, spare) / max(1, len(bands) - 1)
    y = top
    for b, h in zip(bands, heights):
        if b[0]["title"].startswith("Conclusion"):          # the summary sits on a light band
            P.box(M, y - 5, full, h + 10, s["tint"], r=0, z=1)
        band(b, y, True)
        y += h + gap
    if spare < 0:
        problems.append(f"the bands run {-spare:.0f} mm into the footer")

    for k in ("body_pt", "caption_pt", "head_pt", "stat_label_pt"):
        if s[k] < s["min_pt"]:
            problems.append(f"{k} = {s[k]} pt < min {s['min_pt']} pt")
    if not ASSETS.exists():
        print("note: poster/assets/ missing — logos skipped")

    OUT.mkdir(exist_ok=True)
    P.fig.savefig(OUT / "poster.pdf", dpi=300)       # raster figures are resampled to this; text stays vector
    P.fig.savefig(OUT / "poster.png", dpi=preview_dpi)
    print(f"space between bands: {gap:.0f} mm")
    print("band heights (mm): " + "  ".join(f"{b[0]['title'][:12]} {h:.0f}" for b, h in zip(bands, heights)))
    print("entries cited: " + ", ".join(f"E{e}" for e in sorted(used)))
    print(f"wrote {OUT / 'poster.pdf'} and poster.png")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for m in problems:
            print("  ! " + m)
        return 1
    print("checks passed")
    return 0


if __name__ == "__main__":
    dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 60      # optional preview dpi
    sys.exit(build(dpi))
