r"""poster/<name>.md -> poster/out/<name>.pptx: the poster as one editable PowerPoint slide.

Run: uv run --extra dev --with python-pptx==1.0.2 python poster/build_pptx.py [manuscript]

build.py stays the only layout. This script runs it with recording hooks on its drawing calls
(Page.flow, Page.image, and the patch, text, line and image calls on the page axes) and writes each
recorded call as a native shape, so every position on the slide is the one in the PDF:
- a text block (one Page.flow call: paragraph, caption, heading, display equation, header line) is
  one text box in Arial at the PDF size and leading; consecutive blocks of one column and one style
  share a box, one paragraph each, so a bullet list is one box with real bullets;
- inline math ($...$) becomes text runs: italic variables, Unicode Greek and operators, real sub- and
  superscripts; \frac{a}{b} is written inline as a/b. Arial has no glyph for a few relations
  (∝, ≳, ≪, ...); those characters alone are set in Cambria Math, which ships with Office;
- the comparison table is a native table; figures, logos, the header band and the QR are pictures;
  the cards and the key-sentence box are plain rectangles behind the text.

Figures come from poster/out/<set>_600dpi/ when present (python explore/make_poster_figs.py --iqms
--dpi 600 ...), else from the committed 200 dpi PNG with a warning. The check at the end reopens the
file, counts the shapes, gives each picture's resolution at its printed size, and lists text blocks
whose line count, measured in Arial at the box width, differs from the PDF (PowerPoint may wrap
those differently).
"""

from __future__ import annotations

import contextlib
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build as B
import numpy as np
from lxml import etree
from matplotlib.colors import to_hex, to_rgba
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Mm, Pt

FONT = "Arial"
FALLBACK = "Cambria Math"  # only for the characters Arial lacks
NO_ARIAL = set("∝≳≲≪≫∼")
SLACK = 1.0  # mm added to a text box's width, so PowerPoint's wrap does not fall a word short
SUB, SUP = "-25000", "30000"  # baseline shift in thousandths of a percent

# ───────────── recording ─────────────

REC: list[dict] = []
STATE = {"mute": 0, "bullet": False}


def record(kind, z, **kw):
    REC.append(dict(kind=kind, z=float(z), order=len(REC), **kw))


_flow, _image, _init = B.Page.flow, B.Page.image, B.Page.__init__
_bullet, _table = B.bullet, B.table


def flow(
    self, text, x, y, w, pt, color=None, weight="normal", indent=0.0, align="left", z=3, draw=True
):
    STATE["mute"] += 1
    try:
        y1 = _flow(self, text, x, y, w, pt, color, weight, indent, align, z, draw)
    finally:
        STATE["mute"] -= 1
    if draw and not STATE["mute"] and text.strip():
        lh = pt * B.PT_MM * B.SPEC["leading"]
        lines = round((y1 - y - pt * B.PT_MM * 1.35) / lh) + 1
        record(
            "text",
            z,
            text=text,
            x=x,
            y=y,
            w=w,
            pt=pt,
            color=color or B.SPEC["ink"],
            weight=weight,
            indent=indent,
            align=align,
            lines=lines,
            bullet=STATE["bullet"],
        )
    return y1


def image(self, path, x, y, w, h=None, z=2):
    h = _image(self, path, x, y, w, h, z)
    if not STATE["mute"]:
        record("picture", z, path=Path(path), x=x, y=y, w=w, h=h)
    return h


def init(self):
    _init(self)
    ax = self.ax
    add_patch, text, plot, imshow = ax.add_patch, ax.text, ax.plot, ax.imshow

    def rec_patch(p):
        if not (STATE["mute"] or STATE["bullet"]):
            if isinstance(p, Rectangle | FancyBboxPatch):
                if isinstance(p, Rectangle):
                    (x, y), w, h = p.get_xy(), p.get_width(), p.get_height()
                else:
                    x, y, w, h = p.get_x(), p.get_y(), p.get_width(), p.get_height()
                lw = p.get_linewidth()
                record(
                    "rect",
                    p.get_zorder(),
                    x=x,
                    y=y,
                    w=w,
                    h=h,
                    fc=p.get_facecolor(),
                    ec=p.get_edgecolor() if lw > 0 else None,
                    lw=lw,
                    round=isinstance(p, FancyBboxPatch),
                )
            else:
                record("skipped", 0, what=type(p).__name__)
        return add_patch(p)

    def rec_text(x, y, s, **kw):
        if not STATE["mute"]:
            record(
                "label",
                kw.get("zorder", 3),
                x=x,
                y=y,
                text=s,
                pt=kw.get("fontsize", 10),
                color=kw.get("color", B.SPEC["ink"]),
                weight=kw.get("fontweight", "normal"),
                ha=kw.get("ha", "left"),
                va=kw.get("va", "baseline"),
            )
        return text(x, y, s, **kw)

    def rec_plot(xs, ys, *a, **kw):
        if not STATE["mute"]:
            record(
                "line",
                kw.get("zorder", 2),
                xs=list(xs),
                ys=list(ys),
                color=kw.get("color", B.SPEC["ink"]),
                lw=kw.get("lw", 1.0),
            )
        return plot(xs, ys, *a, **kw)

    def rec_imshow(arr, *a, **kw):
        if not STATE["mute"]:
            if "extent" in kw:
                record("array", kw.get("zorder", 1), arr=np.asarray(arr), extent=kw["extent"])
            else:
                record("skipped", 0, what="imshow without extent")
        return imshow(arr, *a, **kw)

    ax.add_patch, ax.text, ax.plot, ax.imshow = rec_patch, rec_text, rec_plot, rec_imshow


def bullet(P, it, x, y, w, draw=True):
    STATE["bullet"] = draw
    try:
        return _bullet(P, it, x, y, w, draw)
    finally:
        STATE["bullet"] = False


def table(P, it, x, y, w, draw=True):
    """Records the table as one item; the geometry mirrors build.table."""
    if not draw:
        return _table(P, it, x, y, w, draw)
    s = B.SPEC
    rows = [list(r) for r in it["rows"]]
    nc = len(rows[0])
    ours = {j for j, c in enumerate(rows[0]) if c.startswith("*")}
    rows[0] = [c.lstrip("*").strip() for c in rows[0]]
    cw = [w * f for f in [0.24] + [0.76 / (nc - 1)] * (nc - 1)]
    cx = [x + sum(cw[:j]) for j in range(nc)]
    pt, px, py = s["body_pt"], 2.5, 2.2
    rhs, yy, lines = [], y, []
    for i, row in enumerate(rows):
        bold = ["bold" if i == 0 or j == 0 else "normal" for j in range(nc)]
        ends = [
            P.flow(c, cx[j] + px, yy + py, cw[j] - 2 * px, pt, weight=bold[j], draw=False)
            for j, c in enumerate(row)
        ]
        rh = max(e - yy for e in ends) + py
        lh = pt * B.PT_MM * s["leading"]
        lines.append([round((e - yy - py - pt * B.PT_MM * 1.35) / lh) + 1 for e in ends])
        rhs.append(rh)
        yy += rh
    STATE["mute"] += 1
    try:
        y1 = _table(P, it, x, y, w, draw)
    finally:
        STATE["mute"] -= 1
    record(
        "table", 3, x=x, y=y, cw=cw, rhs=rhs, rows=rows, ours=ours, pt=pt, px=px, py=py, lines=lines
    )
    return y1


def run_layout(ms):
    B.Page.flow, B.Page.image, B.Page.__init__ = flow, image, init
    B.bullet, B.table = bullet, table
    save, Figure.savefig = Figure.savefig, lambda *a, **k: None
    log = io.StringIO()
    try:
        with contextlib.redirect_stdout(log):
            code = B.build(60, ms)
    finally:
        Figure.savefig = save
    if code:
        print(log.getvalue())
        raise SystemExit("build.py layout reports problems; fix those first")
    return log.getvalue()


# ───────────── math and inline markup -> runs ─────────────

GREEK = {
    **{
        n: chr(0x3B1 + k)
        for k, n in enumerate(
            [
                "alpha",
                "beta",
                "gamma",
                "delta",
                "epsilon",
                "zeta",
                "eta",
                "theta",
                "iota",
                "kappa",
                "lambda",
                "mu",
                "nu",
                "xi",
                "omicron",
                "pi",
                "rho",
                "varsigma",
                "sigma",
                "tau",
                "upsilon",
                "phi",
                "chi",
                "psi",
                "omega",
            ]
        )
    },
    **{
        n: chr(0x391 + k)
        for k, n in enumerate(
            [
                "Alpha",
                "Beta",
                "Gamma",
                "Delta",
                "Epsilon",
                "Zeta",
                "Eta",
                "Theta",
                "Iota",
                "Kappa",
                "Lambda",
                "Mu",
                "Nu",
                "Xi",
                "Omicron",
                "Pi",
                "Rho",
                "_",
                "Sigma",
                "Tau",
                "Upsilon",
                "Phi",
                "Chi",
                "Psi",
                "Omega",
            ]
        )
    },
}
SYMBOL = {
    "partial": "∂",
    "hbar": "ħ",
    "cdot": "·",
    "propto": "∝",
    "gtrsim": "≳",
    "lesssim": "≲",
    "ll": "≪",
    "gg": "≫",
    "leftrightarrow": "↔",
    "approx": "≈",
    "times": "×",
    "sim": "∼",
    "infty": "∞",
    "leq": "≤",
    "geq": "≥",
    "pm": "±",
    "to": "→",
    "rightarrow": "→",
    "ell": "ℓ",
    ",": "\u202f",
    ";": "\u00a0",
    " ": " ",
    "quad": "\u2003",
    "|": "‖",
}
FUNC = {"sin", "cos", "tan", "exp", "ln", "log", "max", "min"}
RELATION = set("=<>∝≳≲≪≫↔≈∼≤≥→")
BINARY = set("+−×·±")
TOK = re.compile(r"\\[A-Za-z]+|\\.|[{}^_]|.")


def parse_math(src):
    toks, pos = TOK.findall(src), 0

    def seq(stop):
        nonlocal pos
        out = []
        while pos < len(toks) and toks[pos] != stop:
            out.append(atom())
        pos += 1  # the closing brace (or past the end)
        return out

    def atom():
        nonlocal pos
        t = toks[pos]
        pos += 1
        if t == "{":
            return ("group", seq("}"))
        if t in "^_":
            return ("sup" if t == "^" else "sub", atom())
        if t.startswith("\\") and t[1:] in ("mathbf", "mathrm", "hat", "text", "boldsymbol"):
            return (t[1:], atom())
        if t == "\\frac":
            return ("frac", atom(), atom())
        return ("tok", t)

    return seq(None)


def emit(nodes, out, level=0, bold=False, upright=False):
    """Flatten parsed math into (text, italic, bold, level, symbol) pieces."""
    for n in nodes:
        kind = n[0]
        if kind == "group":
            emit(n[1], out, level, bold, upright)
        elif kind in ("sup", "sub"):
            emit([n[1]], out, level + (1 if kind == "sup" else -1), bold, upright)
        elif kind in ("mathbf", "boldsymbol"):
            emit([n[1]], out, level, True, True)
        elif kind in ("mathrm", "text"):
            emit([n[1]], out, level, bold, True)
        elif kind == "hat":
            emit([n[1]], out, level, bold, upright)
            out.append(("\u0302", out[-1][1], bold, level, False))
        elif kind == "frac":
            num, den = [], []
            emit([n[1]], num, level, bold, upright)
            emit([n[2]], den, level, bold, upright)
            wrap = sum(len(p[0]) for p in den) > 1
            out += num + [("/", False, bold, level, False)]
            out += ([("(", False, bold, level, False)] if wrap else []) + den
            out += [(")", False, bold, level, False)] if wrap else []
        else:
            t = n[1]
            if t.startswith("\\"):
                name = t[1:]
                if name in ("left", "right"):
                    continue
                if name in GREEK:
                    out.append((GREEK[name], name.islower() and not upright, bold, level, False))
                elif name in SYMBOL:
                    out.append((SYMBOL[name], False, bold, level, True))
                elif name in FUNC:
                    out.append((name, False, bold, level, False))
                else:
                    raise ValueError(f"no text form for \\{name}")
            elif t == "-":
                out.append(("−", False, bold, level, True))
            elif t.isalpha():
                out.append((t, not upright, bold, level, False))
            elif t in "=<>+*":
                out.append((t, False, bold, level, True))
            elif t != " ":
                out.append((t, False, bold, level, False))


def math_pieces(src):
    """Pieces of one $..$ span, with operator spacing on the main line as mathtext sets it:
    relations and binary operators get a no-break space each side, a sign none; no line break
    falls inside the span, as in the PDF."""
    raw = []
    emit(parse_math(src), raw)
    out = []
    for k, (t, it, bd, lv, op) in enumerate(raw):
        prev = raw[k - 1] if k else None
        unary = t in "+−" and (
            prev is None or prev[3] != lv or prev[0] in RELATION | BINARY | set("(,")
        )
        if op and lv == 0 and not unary and (t in RELATION or t in BINARY):
            sp = "\u00a0"
            out += [(sp, False, False, 0), (t, False, bd, 0), (sp, False, False, 0)]
        else:
            out.append((t, it, bd, lv))
    return out


SPAN = re.compile(r"\$[^$]+\$|\*\*[^*]+\*\*")


def runs(text, weight="normal"):
    """(text, italic, bold, level) runs of a manuscript string with $..$ and **..** markup."""
    out, pos = [], 0
    base = weight == "bold"
    for m in SPAN.finditer(text):
        if m.start() > pos:
            out.append((text[pos : m.start()], False, base, 0))
        s = m[0]
        if s.startswith("**"):
            out.append((s[2:-2], False, True, 0))
        else:
            out += math_pieces(s[1:-1])
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, base, 0))
    merged = []
    for r in out:
        if merged and merged[-1][1:] == r[1:]:
            merged[-1] = (merged[-1][0] + r[0], *r[1:])
        else:
            merged.append(r)
    return merged


# ───────────── writing ─────────────


def rgb(c):
    return RGBColor.from_string(to_hex(c)[1:].upper())


def set_font(r_pr, name):
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = r_pr.find(qn(tag))
        if el is None:
            el = etree.SubElement(r_pr, qn(tag))
        el.set("typeface", name)


def add_runs(par, pieces, pt, color, spc=0.0):
    for text, italic, bold, level in pieces:
        # one run per stretch of characters that Arial has, so only the missing ones change face
        for chunk in re.split(f"([{''.join(NO_ARIAL)}])", text):
            if not chunk:
                continue
            r = par.add_run()
            r.text = chunk
            f = r.font
            f.size, f.bold, f.italic = Pt(pt), bold, italic
            f.color.rgb = rgb(color)
            r_pr = r._r.get_or_add_rPr()
            r_pr.set("lang", "en-US")
            if spc:
                r_pr.set("spc", str(round(spc * 100)))
            if level:
                r_pr.set("baseline", SUP if level > 0 else SUB)
            set_font(r_pr, FALLBACK if chunk in NO_ARIAL else FONT)


def frame(tf, wrap=True):
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP


def paragraph(par, rec, space_before=0.0, spc=0.0):
    pt = rec["pt"]
    par.alignment = PP_ALIGN.CENTER if rec["align"] == "center" else PP_ALIGN.LEFT
    par.line_spacing = Pt(pt * B.SPEC["leading"])
    if space_before > 0:
        par.space_before = Pt(space_before / B.PT_MM)
    p_pr = par._p.get_or_add_pPr()
    if rec.get("bullet"):
        p_pr.set("marL", str(Mm(rec["indent"])))
        p_pr.set("indent", str(-Mm(rec["indent"])))
        clr = etree.SubElement(p_pr, qn("a:buClr"))
        etree.SubElement(clr, qn("a:srgbClr")).set("val", to_hex(rec["color"])[1:].upper())
        etree.SubElement(p_pr, qn("a:buSzPct")).set("val", "70000")
        etree.SubElement(p_pr, qn("a:buFont")).set("typeface", FONT)
        etree.SubElement(p_pr, qn("a:buChar")).set("char", "▪")
    else:
        if rec["indent"]:
            p_pr.set("marL", str(Mm(rec["indent"])))
        etree.SubElement(p_pr, qn("a:buNone"))
    add_runs(par, runs(rec["text"], rec["weight"]), pt, rec["color"], spc)


def strip_style(shape):
    """Drop the theme style reference, so no theme shadow or outline comes with a shape."""
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def blocks(recs):
    """Merge consecutive text records of one column and one style into one box."""
    out = []
    for r in recs:
        if r["kind"] != "text":
            out.append(r)
            continue
        prev = out[-1] if out and out[-1]["kind"] == "box" else None
        lh = r["pt"] * B.PT_MM * B.SPEC["leading"]
        if prev:
            last = prev["paras"][-1]
            same = all(
                last[k] == r[k] for k in ("x", "w", "pt", "color", "weight", "align", "bullet")
            )
            gap = r["y"] - (last["y"] + last["lines"] * lh)
            if same and 0 <= gap < 1.5 * lh:
                prev["paras"].append(dict(r, space=gap))
                continue
        out.append({"kind": "box", "z": r["z"], "order": r["order"], "paras": [dict(r, space=0.0)]})
    return out


def hires(path, warn):
    """The 600 dpi render of a committed figure, when make_poster_figs.py --dpi 600 made one."""
    p = Path(path)
    if p.parent.parent == B.ROOT / "figures" / "poster":
        alt = B.OUT / f"{p.parent.name}_600dpi" / p.name
        if alt.exists():
            a0, a1 = Image.open(p).size, Image.open(alt).size
            if abs(a0[1] / a0[0] - a1[1] / a1[0]) > 0.003:
                warn.append(f"{p.name}: the 600 dpi copy has another aspect ratio; kept 200 dpi")
                return p
            return alt
        warn.append(f"{p.name}: no 600 dpi copy in {alt.parent}; used the 200 dpi PNG")
    return p


def write(ms, out):
    s = B.SPEC
    W, H = s["W"], s["H"]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Mm(W), Mm(H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    media = B.OUT / f"{ms.stem}_pptx_media"
    media.mkdir(parents=True, exist_ok=True)
    warn = []
    for r in sorted(blocks(REC), key=lambda r: (r["z"], r["order"])):
        k = r["kind"]
        if k == "rect":
            if r["x"] <= 0 and r["y"] <= 0 and r["w"] >= W and r["h"] >= H:
                slide.background.fill.solid()
                slide.background.fill.fore_color.rgb = rgb(r["fc"])
                continue
            shp = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE if r["round"] else MSO_SHAPE.RECTANGLE,
                Mm(r["x"]),
                Mm(r["y"]),
                Mm(r["w"]),
                Mm(r["h"]),
            )
            strip_style(shp)
            if r["round"]:
                shp.adjustments[0] = min(0.5, 2.5 / min(r["w"], r["h"]))
            if to_rgba(r["fc"])[3] > 0:
                shp.fill.solid()
                shp.fill.fore_color.rgb = rgb(r["fc"])
            else:
                shp.fill.background()
            if r["ec"] is not None:
                shp.line.color.rgb = rgb(r["ec"])
                shp.line.width = Pt(r["lw"])
            else:
                shp.line.fill.background()
            shp.name = f"Box {r['order']}"
        elif k == "line":
            xs, ys = r["xs"], r["ys"]
            for i in range(len(xs) - 1):
                ln = slide.shapes.add_connector(
                    MSO_CONNECTOR.STRAIGHT,
                    Mm(xs[i]),
                    Mm(ys[i]),
                    Mm(xs[i + 1]),
                    Mm(ys[i + 1]),
                )
                strip_style(ln)
                ln.line.color.rgb = rgb(r["color"])
                ln.line.width = Pt(r["lw"])
        elif k in ("picture", "array"):
            if k == "array":
                x0, x1, y1, y0 = r["extent"]
                path = media / f"band_{r['order']}.png"
                a = r["arr"]
                Image.fromarray(
                    (np.clip(a, 0, 1) * 255).astype(np.uint8) if a.dtype.kind == "f" else a
                ).save(path)
                x, y, w, h, alt = x0, y0, x1 - x0, y1 - y0, "header band"
            else:
                path = hires(r["path"], warn)
                x, y, w, h, alt = r["x"], r["y"], r["w"], r["h"], r["path"].stem
            pic = slide.shapes.add_picture(str(path), Mm(x), Mm(y), Mm(w), Mm(h))
            pic.name = f"Picture {alt}"
            pic._element.nvPicPr.cNvPr.set("descr", alt)
        elif k == "label":
            pt = r["pt"]
            top = r["y"] - (pt * B.PT_MM if r["va"] == "baseline" else pt * B.PT_MM / 2)
            width = 0.7 * pt * B.PT_MM * len(r["text"]) + 4
            left = r["x"] - (width / 2 if r["ha"] == "center" else 0)
            tb = slide.shapes.add_textbox(Mm(left), Mm(top), Mm(width), Mm(pt * B.PT_MM * 1.3))
            frame(tb.text_frame, wrap=False)
            rec = {
                "text": r["text"],
                "pt": pt,
                "color": r["color"],
                "weight": r["weight"],
                "align": "center" if r["ha"] == "center" else "left",
                "indent": 0,
            }
            paragraph(tb.text_frame.paragraphs[0], rec)
            tb.name = f"Text {r['text'][:30]}"
        elif k == "box":
            paras = r["paras"]
            first = paras[0]
            lh = first["pt"] * B.PT_MM * s["leading"]
            h = sum(p["space"] + p["lines"] * lh for p in paras)
            x, w = first["x"], first["w"] + SLACK
            if first["align"] == "center":
                x -= SLACK / 2
            tb = slide.shapes.add_textbox(Mm(x), Mm(first["y"]), Mm(w), Mm(h))
            frame(tb.text_frame)
            for i, p in enumerate(paras):
                par = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
                SPC[p["order"]] = spc = fit_spacing(p, w - p["indent"])
                paragraph(par, p, p["space"], spc)
            plain = re.sub(r"\$|\*\*|\\[A-Za-z]+|[{}^_]", "", first["text"])
            tb.name = f"Text {plain[:40]}"
        elif k == "table":
            add_table(slide, r)
        elif k == "skipped":
            warn.append(f"not carried over: {r['what']}")
    prs.save(out)
    return warn


def cell_border(cell, color, width_mm):
    tc_pr = cell._tc.get_or_add_tcPr()
    for k, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = etree.Element(qn(tag))
        if tag == "a:lnB":
            ln.set("w", str(Mm(width_mm)))
            fill = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(fill, qn("a:srgbClr")).set("val", to_hex(color)[1:].upper())
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))
        tc_pr.insert(k, ln)


def add_table(slide, r):
    s = B.SPEC
    rows, cw, rhs = r["rows"], r["cw"], r["rhs"]
    gf = slide.shapes.add_table(
        len(rows), len(cw), Mm(r["x"]), Mm(r["y"]), Mm(sum(cw)), Mm(sum(rhs))
    )
    gf.name = "Table Kinematic vs dynamical"
    tbl = gf.table
    tbl.first_row = tbl.horz_banding = False
    tbl._tbl.tblPr.find(qn("a:tableStyleId")).text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    for j, w in enumerate(cw):
        tbl.columns[j].width = Mm(w)
    for i, row in enumerate(rows):
        tbl.rows[i].height = Mm(rhs[i])
        for j, text in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = Mm(r["px"])
            cell.margin_top, cell.margin_bottom = Mm(r["py"]), Emu(0)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            fc = (
                (s["ours_head"] if j in r["ours"] else s["thead"])
                if i == 0
                else (s["ours"] if j in r["ours"] else None)
            )
            if fc:
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(fc)
            else:
                cell.fill.background()
            cell_border(cell, s["rule"], 0.5)
            par = cell.text_frame.paragraphs[0]
            weight = "bold" if i == 0 or j == 0 else "normal"
            paragraph(
                par,
                {
                    "text": text,
                    "pt": r["pt"],
                    "color": s["ink"],
                    "weight": weight,
                    "align": "left",
                    "indent": 0,
                },
            )


# ───────────── check ─────────────

SPC: dict[int, float] = {}  # character spacing (pt) given to a text record, by its order

FACES = {}


def face(bold, italic, fallback=False):
    key = (bold, italic, fallback)
    if key not in FACES:
        name = (
            "cambria.ttc"
            if fallback
            else {
                (False, False): "arial.ttf",
                (True, False): "arialbd.ttf",
                (False, True): "ariali.ttf",
                (True, True): "arialbi.ttf",
            }[(bold, italic)]
        )
        FACES[key] = ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), 400)
    return FACES[key]


def wrapped_lines(pieces, pt, width_mm, spc=0.0):
    """Greedy word wrap of runs at a box width, Arial metrics: a line count to compare with the
    PDF. Breaks at ordinary spaces only (a no-break space binds), as the PDF layout does; spc
    (pt) is the character spacing."""
    words, cur = [], 0.0
    for text, italic, bold, level in pieces:
        size = pt * (0.67 if level else 1.0)
        for i, part in enumerate(text.split(" ")):
            if i:
                words.append(cur)
                cur = 0.0
            for ch in part:
                f = face(bold, italic, ch in NO_ARIAL)
                cur += (f.getlength(ch) / 400 * size + spc) * B.PT_MM
    words.append(cur)
    space = face(False, False).getlength(" ") / 400 * pt * B.PT_MM
    lines, lw = 1, -space
    for w in words:
        if w == 0:
            continue
        if lw + space + w > width_mm and lw > 0:
            lines, lw = lines + 1, w
        else:
            lw += space + w
    return lines


def fit_spacing(rec, width_mm):
    """Character spacing (pt, 0 or tighter in 0.2 pt steps to -1) at which the block, measured in
    Arial, keeps the line count it has in the PDF, where its math is set in STIX."""
    pieces = runs(rec["text"], rec["weight"])
    for spc in (0.0, -0.2, -0.4, -0.6, -0.8, -1.0):
        if wrapped_lines(pieces, rec["pt"], width_mm, spc) <= rec["lines"]:
            return spc
    return 0.0


def check(out, warn):
    prs = Presentation(out)
    sl = prs.slides[0]
    kinds = {}
    for sh in sl.shapes:
        kinds[sh.shape_type] = kinds.get(sh.shape_type, 0) + 1
    names = {
        MSO_SHAPE_TYPE.TEXT_BOX: "text boxes",
        MSO_SHAPE_TYPE.PICTURE: "pictures",
        MSO_SHAPE_TYPE.AUTO_SHAPE: "rectangles",
        MSO_SHAPE_TYPE.TABLE: "tables",
        MSO_SHAPE_TYPE.LINE: "lines",
    }
    print(
        f"{out.name}: {len(sl.shapes)} shapes, "
        + ", ".join(f"{v} {names.get(k, str(k))}" for k, v in kinds.items())
    )
    print(f"slide {prs.slide_width.mm:.0f} x {prs.slide_height.mm:.0f} mm")
    paras = sum(len(sh.text_frame.paragraphs) for sh in sl.shapes if sh.has_text_frame)
    print(
        f"text: {paras} paragraphs in text boxes; equations and table as native text; "
        "no text set as a picture"
    )
    for sh in sl.shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            px = sh.image.size[0]
            dpi = px / (sh.width.mm / 25.4)
            flag = "" if dpi >= 300 or "header band" in sh.name else "  < 300 dpi"
            print(f"  {sh.name[8:]:24s} {sh.width.mm:6.1f} mm  {dpi:5.0f} dpi{flag}")
    off, tight = [], []
    for r in REC:
        if r["kind"] == "text":
            ind = r["indent"]
            spc = SPC.get(r["order"], 0.0)
            pieces = runs(r["text"], r["weight"])
            got = wrapped_lines(pieces, r["pt"], r["w"] + SLACK - ind, spc)
            if spc:
                tight.append(f"  {spc:+.1f} pt: {r['text'][:60]!r}")
            if got != r["lines"]:
                off.append(f"  {r['lines']} -> {got} lines: {r['text'][:60]!r}")
        elif r["kind"] == "table":
            for i, row in enumerate(r["rows"]):
                for j, c in enumerate(row):
                    if not c:
                        continue
                    wt = "bold" if i == 0 or j == 0 else "normal"
                    got = wrapped_lines(runs(c, wt), r["pt"], r["cw"][j] - 2 * r["px"])
                    if got != r["lines"][i][j]:
                        off.append(f"  table {r['lines'][i][j]} -> {got} lines: {c[:50]!r}")
    print(f"text blocks whose line count in Arial differs from the PDF: {len(off)}")
    print("\n".join(off))
    print(
        f"text blocks set with tighter character spacing to keep the PDF line count: {len(tight)}"
    )
    print("\n".join(tight))
    for m in warn:
        print("warning: " + m)


def main():
    ms = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else B.MS
    run_layout(ms)
    B.OUT.mkdir(exist_ok=True)
    out = B.OUT / f"{ms.stem}.pptx"
    warn = write(ms, out)
    print(f"wrote {out}")
    check(out, warn)


if __name__ == "__main__":
    main()
