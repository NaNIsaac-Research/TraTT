r"""poster/<name>.md -> poster/out/<name>.pdf (+ PNG preview). Run: python poster/build.py [preview_dpi] [manuscript]

Same idea as a print pipeline: the manuscript is canonical and read-only, every coordinate comes
from SPEC (mm, page origin top-left), and the build ends with machine checks. Looking at the PNG
is still required; the checks only catch what a machine can see.

Look (v4, plain). A conventional academic poster: white page, black text in one sans face, one
accent colour for the section titles, no banner, no colour stripe, no tinted boxes, no rules under
the titles. The header holds the title, authors and affiliation with the Sogang IHS shield at the
upper right; the footer holds the acknowledgement, the CUPT logo and the repository QR at the lower
right (logo positions as the advisor asked). One thin grey line separates header and footer from
the body, because the header is no longer a coloured block.

Look "lab" ("look: lab" in the front matter; see LAB). The header, section heads and footer of the
KPS print poster: navy banner with white text and a three-colour stripe, number squares on the
section heads, the key sentence in a tinted box, a tinted Conclusions band, a square-marked
Acknowledgement. "flat: 1" keeps that header and footer but drops the tints and the orange: the
key sentence in a thin navy outline, grey rules under the heads. The body items are the same in
both looks.

Text face: Arial where installed (the lab posters use it), DejaVu Sans otherwise; math in STIX, so
a variable is a serif italic and is told apart from the sans body. Absolute values are
\left|..\right|: a bare STIX | is the height of a lowercase l and reads as one.

Manuscript syntax
  front matter: title ("//" = line break), authors, affiliation, contact, footer, session (header
                  corner), look ("lab" or plain), any SPEC number (e.g. "body_pt: 28");
                  plain only: takehome (one sentence under the title block, tagged), logo_left
                  ("reserved" keeps the upper left free, the session line then goes on top);
                  lab: logo_left is a logo path, set on a white plate in the banner
  "## Title"      a panel (numbered automatically); every panel spans the page width
  "@pair"         the next two panels share one band, side by side
  "[[ 0.5 c" ... "|| 0.5" ... "]]"   a row inside a panel: columns with width fractions; "c"
                  centres that column vertically in the row; rows nest
  "> text"        key sentence, set in the accent colour     "- text"  bullet
  "+ text"        a bold paragraph in body type (a rule the reader should take away)
  "![caption](path)" figure, as wide as its column; path "none" sets the caption as a note
  "~ step | text" input-condition line: a small envelope glyph (step or ramp) followed by the text
  "$$ text"       display line: centred, slightly larger, with space around it (equations)
  {E12}           notebook entry tag (stripped from print, required on every item)

Checks
1. every paragraph, bullet, key sentence and figure carries an {E..} tag, and each tagged Entry
   exists in notes/lab_notebook.md (nothing goes on the poster without its entry);
2. every figure file exists;
3. the bands fit between the header and the footer (no silent reflow);
4. no text below SPEC["min_pt"].

Layout runs twice inside build(): the first pass measures every band, the second spreads the spare
height evenly between the bands, so the last one ends level with the footer.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
for _f in sorted((ROOT / "poster" / "fonts").glob("*.ttf")):
    font_manager.fontManager.addfont(str(_f))

FONT = os.environ.get("TRATT_FONT") or next(
    (
        f
        for f in ("Arial", "DejaVu Sans")
        if f in {x.name for x in font_manager.fontManager.ttflist}
    ),
    "DejaVu Sans",
)
MATH = os.environ.get("TRATT_MATH", "stix")
matplotlib.rcParams.update(
    {
        # Word-by-word placement needs text widths that scale linearly with dpi; hinting breaks
        # that and makes long words overrun the next one in a preview rendered at another dpi.
        "text.hinting": "none",
        "text.hinting_factor": 1,
        "font.family": FONT,
        "pdf.fonttype": 42,  # TrueType in the PDF: editable, accepted by print shops
        "mathtext.fontset": MATH,
    }
)
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

MS = ROOT / "poster" / "poster.md"
OUT = ROOT / "poster" / "out"
ASSETS = ROOT / "poster" / "assets"
NOTEBOOK = ROOT / "notes" / "lab_notebook.md"

# A0 portrait (841 x 1189 mm), as the ICAMD 2025 and KPS 2026 posters.
SPEC = dict(
    W=841,
    H=1189,
    margin=18,
    gap=14,
    pad=6,
    header_h=92,
    footer_h=54,  # QR 40 mm
    title_pt=52,
    takehome_pt=34,
    authors_pt=30,
    affil_pt=24,
    head_pt=36,
    body_pt=25,
    key_pt=26,
    caption_pt=22,
    eq_pt=27,
    min_pt=22,
    leading=1.25,
    para_gap=6,
    panel_gap=8,
    fig_gap=4,
    spread_max=3,
    accent="#1f4e8c",
    page="#ffffff",
    ink="#1a1a1a",
    ink2="#4a4a4a",
    line="#bdbdbd",
)
# "look: lab" in the front matter: the lab template of the KPS print poster (Oct 19, commit
# a7747b0): navy header band on the lab banner with white text and a three-colour stripe, number
# squares on the section heads, the key sentence in a tinted box, a tinted Conclusions band and a
# square-marked Acknowledgement. Geometry and colours are taken from that build.
LAB = dict(
    header_h=110,
    stripe_h=5,
    footer_h=53,
    navy="#0f2a3a",
    orange="#e8743b",
    key_soft="#fcf5e6",
    zone_end="#f4f5f3",
    edge="#c3c9ce",
    rule="#a9b2b9",
    rule_w=0.4,
    callout_pt=29,
    stripe=("#3a3a3a", "#e04b3a", "#f08a3c"),
    # "flat: 1": white body, navy the only accent: the key sentence in a thin navy outline, grey
    # rules under the section heads, no tinted Conclusions band (header and footer unchanged)
    flat=0,
)
LOOK = {"lab": False}
PT_MM = 25.4 / 72
XH = {"Arial": 0.519, "DejaVu Sans": 0.545}.get(FONT, 0.52)  # x-height / em


# ───────────── manuscript ─────────────

TAG = re.compile(r"\{E(\d+)\}")


def squash(text):
    """Collapse ASCII whitespace only: a no-break space (U+00A0) keeps "Si 440" on one line."""
    return re.sub(r"[ \t\r\n]+", " ", text).strip()


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
                b = squash(b)
                add(dict(kind="bullet", text=TAG.sub("", b).strip(), tags=TAG.findall(b)))
            continue
        if block.startswith("~"):
            shape, t = block[1:].split("|", 1)
            t = squash(t)
            add(
                dict(
                    kind="onset",
                    shape=shape.strip(),
                    text=TAG.sub("", t).strip(),
                    tags=TAG.findall(t),
                )
            )
            continue
        if block.startswith("$$"):
            t = squash(block[2:])
            add(dict(kind="eq", text=TAG.sub("", t).strip(), tags=TAG.findall(t)))
            continue
        kind = {">": "key", "+": "strong"}.get(block[0], "para")
        t = squash(re.sub(r"^[>+]\s?", "", block, flags=re.M) if kind != "para" else block)
        add(dict(kind=kind, text=TAG.sub("", t).strip(), tags=TAG.findall(t)))
    return meta, panels


# ───────────── typesetting ─────────────

# a lone * is a word; only ASCII whitespace separates words, so U+00A0 binds "Si 440"
TOKEN = re.compile(r"\$[^$]+\$|\*\*[^*]+\*\*|[^ \t\r\n$*]+|\*")


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

    def flow(
        self,
        text,
        x,
        y,
        w,
        pt,
        color=None,
        weight="normal",
        indent=0.0,
        align="left",
        z=3,
        draw=True,
    ):
        """Word-by-word placement with wrapping; $..$ and **..** stay atomic, **..** is bold.
        Returns the y (mm) just below the last line."""
        color = color or SPEC["ink"]
        lh = pt * PT_MM * SPEC["leading"]
        sp = self.width("a a", pt) - 2 * self.width("a", pt)
        y = y + pt * PT_MM  # baseline of the first line
        toks, prev = [], 0
        for m in TOKEN.finditer(text):
            glue = m.start() == prev and bool(toks)
            prev = m.end()
            s, wgt = m[0], weight
            if s.startswith("**"):
                s, wgt = s[2:-2], "bold"
            toks.append((s, wgt, glue))
        lines, line, lw = [], [], 0.0
        for s, wgt, g in toks:
            tw = self.width(s, pt, wgt)
            add = tw + (0 if g or not line else sp)
            if line and lw + add > w - indent:
                k = len(line)  # a glued run ending the line moves along
                while g and k > 1 and line[k - 1][2]:
                    k -= 1
                if g:
                    k -= 1
                carry = line[k:] if k > 0 else []
                kept = line[:k] if k > 0 else line
                lines.append(
                    (kept, sum(t[3] for t in kept) + sp * sum(1 for t in kept[1:] if not t[2]))
                )
                line = [(cs, cw, i > 0 and cg, ctw) for i, (cs, cw, cg, ctw) in enumerate(carry)]
                lw = sum(t[3] for t in line) + sp * sum(1 for t in line[1:] if not t[2])
                add = tw if not line else tw + (0 if g else sp)
            line.append((s, wgt, g if line else False, tw))
            lw += add
        if line:
            lines.append((line, lw))
        for line, lw in lines:
            cx = x + indent + ((w - indent - lw) / 2 if align == "center" else 0)
            first = True
            for s, wgt, g, tw in line:
                if not g and not first:
                    cx += sp
                if draw:
                    self.ax.text(
                        cx,
                        y,
                        s,
                        fontsize=pt,
                        color=color,
                        family=FONT,
                        zorder=z,
                        fontweight=wgt,
                        va="baseline",
                    )
                cx += tw
                first = False
            y += lh
        return y - lh + pt * PT_MM * 0.35 if lines else y - pt * PT_MM

    def image(self, path, x, y, w, h=None, z=2):
        """Place an image at (x, y) mm, width w; height from the aspect ratio unless given."""
        img = mpimg.imread(path)
        h = h or w * img.shape[0] / img.shape[1]
        a = self.fig.add_axes(
            [x / SPEC["W"], 1 - (y + h) / SPEC["H"], w / SPEC["W"], h / SPEC["H"]], zorder=z
        )
        a.imshow(img, cmap="gray", interpolation="lanczos")
        a.axis("off")
        return h

    def rect(self, x, y, w, h, fc, z=1):
        self.ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec="none", lw=0, zorder=z))


# ───────────── items ─────────────


def bullet(P, it, x, y, w, draw=True):
    s = SPEC
    if draw:
        d = s["body_pt"] * PT_MM * 0.22  # marker side
        mid = y + s["body_pt"] * PT_MM * (1 - XH / 2)  # middle of the x-height of the first line
        P.rect(x + 0.5, mid - d / 2, d, d, s["ink"], z=3)
    return P.flow(it["text"], x, y, w, s["body_pt"], indent=6, draw=draw) + s["para_gap"]


def key(P, it, x, y, w, draw=True):
    s = SPEC
    if LOOK["lab"]:  # tinted box with an orange edge, as on the print poster
        y1 = P.flow(it["text"], x + 10, y + 9, w - 20, s["callout_pt"], s["ink"], draw=draw) + 8
        if draw and s["flat"]:
            for bx, by, bw, bh in (
                (x, y, w, 0.5),
                (x, y1 - 0.5, w, 0.5),
                (x, y, 0.5, y1 - y),
                (x + w - 0.5, y, 0.5, y1 - y),
            ):
                P.rect(bx, by, bw, bh, s["navy"], z=2)
        elif draw:
            P.rect(x, y, w, y1 - y, s["key_soft"], z=2)
            P.rect(x, y, 1.4, y1 - y, s["orange"], z=2)
        return y1 + s["para_gap"]
    return P.flow(it["text"], x, y, w, s["key_pt"], s["accent"], draw=draw) + s["para_gap"]


def equation(P, it, x, y, w, draw=True):
    s = SPEC
    return (
        P.flow(it["text"], x, y + 1, w, s["eq_pt"], align="center", draw=draw) + s["para_gap"] + 1.5
    )


def onset(P, it, x, y, w, draw=True):
    """Input condition of a result panel on one line: envelope glyph A(s) (step or linear ramp,
    onset at s = 0), then the condition in body type."""
    s = SPEC
    gw, x0, top, base = 46.0, x + 11.0, y + 3.0, y + 12.5  # glyph width, onset, A = 1, A = 0
    knee = x0 + (17.0 if it["shape"] == "ramp" else 0.0)
    lab = s["caption_pt"] * PT_MM
    if draw:
        P.ax.annotate(
            "",
            xy=(x + gw, base),
            xytext=(x, base),
            zorder=3,
            arrowprops=dict(arrowstyle="-|>", color=s["ink2"], lw=1.4, mutation_scale=14),
        )
        P.ax.plot(
            [x, x0, knee, x + gw - 6],
            [base, base, top, top],
            color=s["ink"],
            lw=3.0,
            solid_joinstyle="miter",
            zorder=4,
        )
        P.ax.text(
            x + gw + 1.2,
            base,
            "$s$",
            fontsize=s["caption_pt"],
            color=s["ink2"],
            va="center",
            zorder=4,
        )
        ticks = [(x0, "$0$")] + ([(knee, "$T_{rise}$")] if knee > x0 else [])
        for tx, t in ticks:
            P.ax.plot([tx, tx], [base, base + 1.6], color=s["ink2"], lw=1.4, zorder=3)
            P.ax.text(
                tx,
                base + 2.0,
                t,
                fontsize=s["caption_pt"],
                color=s["ink2"],
                ha="center",
                va="top",
                zorder=4,
            )
        if knee > x0:
            P.ax.plot([knee, knee], [top, base], color=s["ink2"], lw=1.0, ls=(0, (2, 2)), zorder=3)
    y1 = P.flow(it["text"], x + gw + 9, y + 0.6, w - gw - 9, s["body_pt"], draw=draw)
    return max(y1, base + 2.0 + lab) + s["para_gap"]


def aspect(path):
    a = mpimg.imread(path)
    return a.shape[0] / a.shape[1]


def items(P, its, x, y, w, draw, check, spread=0.0):
    """Lay out a list of items in the column (x, w) from y down; returns the y below the last one.
    With draw=False nothing is drawn, so the same call measures. check(it) records tag problems.
    `spread` (mm) is added between consecutive items, to even out the two panels of a band; the
    condition line keeps its place under the head, so both panels start alike."""
    s = SPEC
    for i, it in enumerate(its):
        if i and its[i - 1]["kind"] != "onset":
            y += spread
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
            hs = [
                items(P, c["items"], cx_, 0.0, w_, False, check)
                for c, cx_, w_ in zip(it["cols"], xs, ws, strict=True)
            ]
            rh = max(hs)
            if draw:
                for c, cx_, w_, h_ in zip(it["cols"], xs, ws, hs, strict=True):
                    top = y + ((rh - h_) / 2 if c["center"] else 0.0)
                    items(P, c["items"], cx_, top, w_, True, check)
            y += rh
        elif k == "fig":
            f = ROOT / it["path"]
            if it["path"] == "none":  # "![text](none)": a caption-size note
                y = P.flow(it["caption"], x, y, w, s["caption_pt"], s["ink2"], draw=draw)
                y += s["para_gap"]
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
        elif k == "key":
            y = key(P, it, x, y, w, draw)
        elif k == "eq":
            y = equation(P, it, x, y, w, draw)
        elif k == "onset":
            y = onset(P, it, x, y, w, draw)
        elif k == "strong":
            y = P.flow(it["text"], x, y, w, s["body_pt"], weight="bold", draw=draw) + s["para_gap"]
        else:
            y = P.flow(it["text"], x, y, w, s["body_pt"], draw=draw) + s["para_gap"]
    return y


HEAD = 24.0  # section title and the space under it
HEAD_LAB = 32.0  # number square, title and rule


def head(P, num, title, x, y0, w):
    s = SPEC
    if not LOOK["lab"]:
        P.flow(f"{num}  {title}", x, y0, w, s["head_pt"], s["accent"], weight="bold")
        return
    sq = 12.1
    P.rect(x, y0 + 4, sq, sq, s["navy"], z=3)
    P.ax.text(
        x + sq / 2,
        y0 + 4 + sq / 2,
        str(num),
        fontsize=23.2,
        color="white",
        family=FONT,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=4,
    )
    P.flow(title, x + sq + 4.5, y0 + 0.5, w - sq - 4.5, s["head_pt"], s["ink"], weight="bold")
    if s["flat"]:
        P.rect(x, y0 + 24, w, s["rule_w"], s["rule"], z=3)
        return
    P.rect(x, y0 + 24, w * 0.88, s["rule_w"], s["rule"], z=3)
    P.rect(x + w * 0.88, y0 + 24, w * 0.12, s["rule_w"], s["orange"], z=3)


def fit(P, path, x, y, w, h, align="right"):
    """Largest copy of an image inside the box (x, y, w, h), centred vertically; returns its width."""
    img = mpimg.imread(path)
    a = img.shape[0] / img.shape[1]
    iw = min(w, h / a)
    P.image(path, x + (w - iw if align == "right" else 0), y + (h - iw * a) / 2, iw, h=iw * a)
    return iw


# ───────────── page ─────────────


def header_plain(P, meta, tagged):
    """Plain look: title block on white, the shield at the upper right, a grey rule under it.
    Returns the y of that rule."""
    s, ax = SPEC, P.ax
    W, M = s["W"], s["margin"]
    logo_w = 0
    if (ASSETS / "logo_ihs.png").exists():
        logo_w = 62
        fit(P, ASSETS / "logo_ihs.png", W - M - 52, 12, 52, s["header_h"] - 24)
    # "logo_left: reserved" keeps the upper left corner free for a logo still to come; the session
    # line then moves to the top centre, above the title
    left = meta.get("logo_left")
    if left and (ROOT / left).exists():
        fit(P, ROOT / left, M + s["pad"], 12, 52, s["header_h"] - 24, align="left")
    shift = 0.0
    if meta.get("session") and left:
        P.flow(
            meta["session"],
            M + logo_w,
            6,
            W - 2 * M - 2 * logo_w,
            s["caption_pt"],
            s["ink2"],
            align="center",
        )
        shift = 8.0
    elif meta.get("session"):
        P.flow(meta["session"], M + s["pad"], 10, 150, s["caption_pt"], s["ink2"])
    tw = W - 2 * M - 2 * logo_w
    y = 16 + shift - s["title_pt"] * PT_MM * (s["leading"] - 1)
    for line in meta.get("title", "").split("//"):  # "//" in the title = manual line break
        y = (
            P.flow(
                line.strip(),
                M + logo_w,
                y + s["title_pt"] * PT_MM * (s["leading"] - 1),
                tw,
                s["title_pt"],
                s["ink"],
                weight="bold",
                align="center",
            )
            - s["title_pt"] * PT_MM * 0.35
        )
    y = P.flow(meta.get("authors", ""), M + logo_w, y + 8, tw, s["authors_pt"], align="center")
    y = P.flow(
        meta.get("affiliation", ""), M + logo_w, y + 2, tw, s["affil_pt"], s["ink2"], align="center"
    )
    header_h = s["header_h"] + shift
    if meta.get("takehome"):  # the poster's one sentence, under the title block in large type
        t = meta["takehome"]
        tagged(TAG.findall(t), "takehome line")
        y = P.flow(
            TAG.sub("", t).strip(),
            M + s["pad"],
            y + 6,
            W - 2 * (M + s["pad"]),
            s["takehome_pt"],
            s["accent"],
            weight="bold",
            align="center",
        )
        header_h = max(header_h, y + 6)
    ax.plot(
        [M + s["pad"], W - M - s["pad"]],
        [header_h, header_h],
        color=s["line"],
        lw=1.0,
        zorder=2,
    )
    return header_h


def footer_plain(P, meta, problems):
    """Plain look: acknowledgement, CUPT logo and repository QR under a grey rule; returns its y."""
    s, ax = SPEC, P.ax
    W, H, M = s["W"], s["H"], s["margin"]
    fy = H - s["footer_h"]
    ax.plot([M + s["pad"], W - M - s["pad"]], [fy, fy], color=s["line"], lw=1.0, zorder=2)
    qr = ASSETS / "qr_repo.png"
    if not qr.exists():
        qr = ROOT / "figures" / "poster" / "qr_repo.png"
    qr_w = s["footer_h"] - 14.0
    qr_x = W - M - s["pad"] - qr_w
    if qr.exists():
        P.image(qr, qr_x, fy + 7, qr_w, h=qr_w)
    else:
        problems.append("missing footer QR")
    cupt_left = qr_x - 16.0 - 115.0
    if (ASSETS / "logo_cupt.png").exists():
        fit(P, ASSETS / "logo_cupt.png", cupt_left, fy + 7, 115.0, s["footer_h"] - 14)
    else:
        problems.append("missing CUPT footer logo")
    yk = P.flow(
        "Acknowledgement",
        M + s["pad"],
        fy + 8,
        cupt_left - M - s["pad"] - 20,
        s["caption_pt"] + 4,
        s["accent"],
        weight="bold",
    )
    tx, tw = M + s["pad"], cupt_left - M - s["pad"] - 20
    yk = P.flow(meta.get("footer", ""), tx, yk + 1, tw, s["caption_pt"] + 1, s["ink"])
    # the repository line stands apart from the grant text, next to the QR it describes
    P.flow(meta.get("contact", ""), tx, yk + 2, tw, s["caption_pt"] + 1, s["ink"])
    return fy


def header_lab(P, meta):
    """Lab look: navy band on the lab banner, white title block, the shield at the right, session
    line at the upper left, three-colour stripe under the band. An optional logo_left (a path) sits
    on a white plate at the upper left, the session line then under it. Returns the y below the stripe."""
    s, ax = SPEC, P.ax
    W, H, M = s["W"], s["H"], s["margin"]
    hh = s["header_h"]
    ax.add_patch(plt.Rectangle((0, 0), W, hh, color=s["navy"], lw=0, zorder=1))
    if (ASSETS / "header_bg.png").exists():  # drawn for 130 mm; trim rows, never stretch
        bg = mpimg.imread(ASSETS / "header_bg.png")
        keep = min(bg.shape[0], round(bg.shape[0] * hh / 130))
        top = (bg.shape[0] - keep) // 2
        ax.imshow(
            bg[top : top + keep],
            extent=(0, W, hh, 0),
            aspect="auto",
            zorder=1.5,
            interpolation="lanczos",
        )
        ax.set_xlim(0, W)
        ax.set_ylim(H, 0)
    seg = (0.0, 0.58, 0.60, 0.84, 0.86, 1.0)
    for i, c in enumerate(s["stripe"]):
        P.rect(seg[2 * i] * W, hh + 2, (seg[2 * i + 1] - seg[2 * i]) * W, s["stripe_h"], c, z=1)
    logo_w = 0
    if (ASSETS / "logo_ihs.png").exists():  # size and inset of the print poster
        logo_w = 100
        P.image(ASSETS / "logo_ihs.png", W - 22.4 - 55.4, (hh - 79.7) / 2, 55.4, h=79.7)
    left = meta.get("logo_left")
    session_y = 14
    if left and (ROOT / left).exists():  # conference logo on a white plate, session line under it
        P.rect(M + 6, 12, 120, 32, "white", z=2)
        fit(P, ROOT / left, M + 9, 14, 114, 28, align="left")
        session_y = 50
    if meta.get("session"):
        P.flow(meta["session"], M + 6, session_y, 150, s["caption_pt"], "white")
    tw = W - 2 * M - 2 * logo_w
    y = 15 - s["title_pt"] * PT_MM * (s["leading"] - 1)
    for line in meta.get("title", "").split("//"):
        y = (
            P.flow(
                line.strip(),
                M + logo_w,
                y + s["title_pt"] * PT_MM * (s["leading"] - 1),
                tw,
                s["title_pt"],
                "white",
                weight="bold",
                align="center",
            )
            - s["title_pt"] * PT_MM * 0.35
        )
    y = P.flow(
        meta.get("authors", ""), M + logo_w, y + 13, tw, s["authors_pt"], "white", align="center"
    )
    P.flow(
        meta.get("affiliation", ""), M + logo_w, y + 4, tw, s["affil_pt"], "#c9d6e0", align="center"
    )
    return hh + s["stripe_h"] + 2


def footer_lab(P, meta, problems):
    """Lab look: square-marked Acknowledgement, grant and repository lines, CUPT logo and
    QR at the lower right. Returns the y of the hairline above it."""
    s, ax = SPEC, P.ax
    W, H, M = s["W"], s["H"], s["margin"]
    fy = H - s["footer_h"]
    ax.plot([M, W - M], [fy - 1.4, fy - 1.4], color=s["edge"], lw=0.8, zorder=2)
    left = M + s["pad"]
    base, sq = fy + 17.5, 6.7
    P.rect(left, base - sq + 0.4, sq, sq, s["navy"], z=3)
    ax.text(
        left + sq + 3.2,
        base,
        "Acknowledgement",
        fontsize=s["head_pt"] - 6,
        color=s["ink"],
        family=FONT,
        fontweight="bold",
        va="baseline",
        zorder=3,
    )
    qr = ASSETS / "qr_repo.png"
    if not qr.exists():
        qr = ROOT / "figures" / "poster" / "qr_repo.png"
    qr_w = min(37.0, s["footer_h"] - 12.0)
    qr_x = W - M - qr_w - 1.5
    if qr.exists():
        P.image(qr, qr_x, fy + (s["footer_h"] - qr_w) / 2, qr_w, h=qr_w)
    else:
        problems.append("missing footer QR")
    cupt_left = qr_x - 16.0 - 115.0
    if (ASSETS / "logo_cupt.png").exists():
        fit(P, ASSETS / "logo_cupt.png", cupt_left, fy + 7, 115.0, s["footer_h"] - 14)
    else:
        problems.append("missing CUPT footer logo")
    y = fy + 21.0
    for k in ("footer", "contact"):  # grant, then the repository the QR points to
        y = P.flow(meta.get(k, ""), left, y, cupt_left - left - 22, s["caption_pt"] + 1, s["ink"])
    return fy - 1.4


def build(preview_dpi=60, ms=MS):
    s = SPEC
    meta, panels = parse(ms.read_text(encoding="utf8"))
    LOOK["lab"] = meta.get("look") == "lab"
    if LOOK["lab"]:
        SPEC.update(LAB)
    # a SPEC number in the front matter (e.g. "body_pt: 28") holds for this manuscript; one build
    # per process, and every item function reads SPEC
    SPEC.update({k: float(v) for k, v in meta.items() if isinstance(SPEC.get(k), int | float)})
    known = set(
        re.findall(r"^## .*?Entry (\d+)\b", NOTEBOOK.read_text(encoding="utf8"), flags=re.M)
    )
    problems, used = [], set()
    P = Page()
    ax = P.ax
    W, H, M = s["W"], s["H"], s["margin"]
    ax.add_patch(plt.Rectangle((0, 0), W, H, color=s["page"], lw=0, zorder=0))

    def tagged(tags, what):
        if not tags:
            problems.append(f"untagged {what}")
        for t in tags:
            used.add(int(t))
            if t not in known:
                problems.append(f"tag E{t} is not an Entry in the notebook")

    if LOOK["lab"]:
        header_h = header_lab(P, meta)
        fy = footer_lab(P, meta, problems)
    else:
        header_h = header_plain(P, meta, tagged)
        fy = footer_plain(P, meta, problems)

    def check(it):
        if it["tags"] is None:  # rows carry no tag; their items do
            return
        tagged(it["tags"], f"{it['kind']}: {it.get('text', it.get('caption', ''))[:50]!r}")
        if it["kind"] == "fig" and it["path"] != "none" and not (ROOT / it["path"]).exists():
            problems.append(f"missing figure {it['path']}")

    bands = []
    for p in panels:
        if p["group"] is not None and bands and bands[-1][0]["group"] == p["group"]:
            bands[-1].append(p)
        else:
            bands.append([p])
    top = header_h + s["panel_gap"] + 4
    bottom = fy - 6
    full = W - 2 * M

    panel_h = {}  # measured height of each panel (mm), printed to balance a pair
    hd = HEAD_LAB if LOOK["lab"] else HEAD

    def band(b, y0, draw):
        n = len(b)
        pw = (full - (n - 1) * 2 * s["gap"]) / n
        ends = []
        hs = [items(P, p["items"], 0.0, 0.0, pw - 2 * s["pad"], False, check) for p in b]
        if not draw:
            panel_h.update({p["title"]: h + hd for p, h in zip(b, hs, strict=True)})
        for k, p in enumerate(b):
            x = M + s["pad"] + k * (pw + 2 * s["gap"])
            w = pw - 2 * s["pad"]
            if draw:
                head(P, number[id(p)], p["title"], x, y0, w)
            # side by side, the shorter panel spreads its slack over its item gaps (capped), so the
            # two columns end near the same line instead of leaving a hole under one of them
            spread = (
                min(
                    s["spread_max"],
                    (max(hs) - hs[k])
                    / max(1, sum(it["kind"] != "onset" for it in p["items"][:-1])),
                )
                if n == 2
                else 0.0
            )
            ends.append(items(P, p["items"], x, y0 + hd, w, draw, check, spread))
        return max(ends) - s["para_gap"]

    number = {id(p): k + 1 for k, p in enumerate(panels)}
    heights = [band(b, 0.0, False) for b in bands]
    spare = bottom - top - sum(heights) - s["panel_gap"] * (len(bands) - 1)
    gap = s["panel_gap"] + max(0.0, spare) / max(1, len(bands) - 1)
    y = top
    for b, h in zip(bands, heights, strict=True):
        if (
            LOOK["lab"] and not s["flat"] and b[0]["title"].startswith("Conclusion")
        ):  # tinted to the footer line
            z0 = y - min(gap / 2, 12.0)
            ax.add_patch(plt.Rectangle((0, z0), W, fy - z0, color=s["zone_end"], lw=0, zorder=0.5))
        band(b, y, True)
        y += h + gap
    if spare < 0:
        problems.append(f"the bands run {-spare:.0f} mm into the footer")

    for k in ("body_pt", "caption_pt", "head_pt", "key_pt", "eq_pt"):
        if s[k] < s["min_pt"]:
            problems.append(f"{k} = {s[k]} pt < min {s['min_pt']} pt")
    if not ASSETS.exists():
        print("note: poster/assets/ missing — logos skipped")

    OUT.mkdir(exist_ok=True)
    P.fig.savefig(OUT / f"{ms.stem}.pdf", dpi=300)  # raster figures are resampled to this
    P.fig.savefig(OUT / f"{ms.stem}.png", dpi=preview_dpi)
    print(f"font: {FONT}; space between bands: {gap:.0f} mm")
    print(
        "band heights (mm): "
        + "  ".join(f"{b[0]['title'][:12]} {h:.0f}" for b, h in zip(bands, heights, strict=True))
    )
    print("panel heights (mm): " + "  ".join(f"{t[:12]} {h:.0f}" for t, h in panel_h.items()))
    print("entries cited: " + ", ".join(f"E{e}" for e in sorted(used)))
    print(f"wrote {OUT / ms.stem}.pdf and .png")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for m in problems:
            print("  ! " + m)
        return 1
    print("checks passed")
    return 0


if __name__ == "__main__":
    dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 60  # optional preview dpi
    ms = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else MS  # e.g. poster/iqms.md
    sys.exit(build(dpi, ms))
