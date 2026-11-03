import math
from bisect import bisect_right
from fontTools.pens.recordingPen import RecordingPen

_STEPS = 16
_TS = [i / _STEPS for i in range(_STEPS + 1)]
_WEIGHTS = [((1.0 - t)**3, 3.0 * (1.0 - t)**2 * t, 3.0 * (1.0 - t) * t**2, t**3) for t in _TS]


def split_cubic_at(p0, p1, p2, p3, t):
    u = t
    mu = 1.0 - u
    p01 = (mu * p0[0] + u * p1[0], mu * p0[1] + u * p1[1])
    p12 = (mu * p1[0] + u * p2[0], mu * p1[1] + u * p2[1])
    p23 = (mu * p2[0] + u * p3[0], mu * p2[1] + u * p3[1])
    p012 = (mu * p01[0] + u * p12[0], mu * p01[1] + u * p12[1])
    p123 = (mu * p12[0] + u * p23[0], mu * p12[1] + u * p23[1])
    p0123 = (mu * p012[0] + u * p123[0], mu * p012[1] + u * p123[1])
    return (p0, p01, p012, p0123), (p0123, p123, p23, p3)


def split_cubic_interval(p0, p1, p2, p3, t0, t1):
    if t0 <= 1e-7 and t1 >= 1.0 - 1e-7:
        return (p0, p1, p2, p3)
    if t0 > 1e-7:
        _, right = split_cubic_at(p0, p1, p2, p3, t0)
        p0, p1, p2, p3 = right
        t1_adj = (t1 - t0) / (1.0 - t0) if (1.0 - t0) > 1e-9 else 1.0
    else:
        t1_adj = t1
    if t1_adj < 1.0 - 1e-7:
        left, _ = split_cubic_at(p0, p1, p2, p3, t1_adj)
        return left
    return (p0, p1, p2, p3)


def unit_vec(dx, dy):
    n = math.hypot(dx, dy)
    if n < 1e-9:
        return (0.0, 0.0)
    return (dx / n, dy / n)


def _cubic_start_tan(p0, p1, p2, p3):
    for q in (p1, p2, p3):
        v = unit_vec(q[0] - p0[0], q[1] - p0[1])
        if v != (0.0, 0.0):
            return v
    return (0.0, 0.0)


def _cubic_end_tan(p0, p1, p2, p3):
    for q in (p2, p1, p0):
        v = unit_vec(p3[0] - q[0], p3[1] - q[1])
        if v != (0.0, 0.0):
            return v
    return (0.0, 0.0)


class Segment:
    __slots__ = ('kind', 'pts', 'length', '_dists')

    def __init__(self, kind, pts):
        self.kind = kind
        self.pts = pts
        if kind == 'line':
            p0, p1 = pts
            self.length = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            self._dists = None
        else:
            p0, p1, p2, p3 = pts
            p0x, p0y = p0
            p1x, p1y = p1
            p2x, p2y = p2
            p3x, p3y = p3
            dists = [0.0]
            prev_x, prev_y = p0x, p0y
            acc = 0.0
            for k in range(1, _STEPS + 1):
                w0, w1, w2, w3 = _WEIGHTS[k]
                cx = w0 * p0x + w1 * p1x + w2 * p2x + w3 * p3x
                cy = w0 * p0y + w1 * p1y + w2 * p2y + w3 * p3y
                acc += math.hypot(cx - prev_x, cy - prev_y)
                dists.append(acc)
                prev_x, prev_y = cx, cy
            self._dists = dists
            self.length = acc

    @property
    def start(self):
        return self.pts[0]

    @property
    def end(self):
        return self.pts[-1]

    def start_tangent(self):
        if self.kind == 'line':
            p0, p1 = self.pts
            return unit_vec(p1[0] - p0[0], p1[1] - p0[1])
        return _cubic_start_tan(*self.pts)

    def end_tangent(self):
        if self.kind == 'line':
            p0, p1 = self.pts
            return unit_vec(p1[0] - p0[0], p1[1] - p0[1])
        return _cubic_end_tan(*self.pts)

    def _d_to_t(self, d):
        if d <= 0.0:
            return 0.0
        if d >= self.length:
            return 1.0
        dists = self._dists
        idx = bisect_right(dists, d) - 1
        idx = max(0, min(_STEPS - 1, idx))
        d0 = dists[idx]
        d1 = dists[idx + 1]
        span = d1 - d0
        frac = (d - d0) / span if span > 1e-9 else 0.0
        return (idx + frac) / _STEPS

    def point_and_tangent_at_dist(self, d):
        if self.length < 1e-7:
            return self.start, self.start_tangent()
        if self.kind == 'line':
            u = max(0.0, min(1.0, d / self.length))
            p0, p1 = self.pts
            pt = (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u)
            return pt, self.start_tangent()
        else:
            t = self._d_to_t(d)
            p0, p1, p2, p3 = self.pts
            left, right = split_cubic_at(p0, p1, p2, p3, t)
            pt = left[3]
            tan = _cubic_start_tan(*right) if t < 0.999 else _cubic_end_tan(*left)
            return pt, tan

    def subsegment_by_dist(self, d0, d1):
        if d1 - d0 <= 1e-4 or self.length < 1e-7:
            return None
        if self.kind == 'line':
            p0, p1 = self.pts
            u0 = max(0.0, min(1.0, d0 / self.length))
            u1 = max(0.0, min(1.0, d1 / self.length))
            if u1 - u0 <= 1e-5:
                return None
            q0 = (p0[0] + (p1[0] - p0[0]) * u0, p0[1] + (p1[1] - p0[1]) * u0)
            q1 = (p0[0] + (p1[0] - p0[0]) * u1, p0[1] + (p1[1] - p0[1]) * u1)
            return Segment('line', (q0, q1))
        else:
            t0 = self._d_to_t(d0)
            t1 = self._d_to_t(d1)
            if t1 - t0 <= 1e-5:
                return None
            p0, p1, p2, p3 = self.pts
            return Segment('cubic', split_cubic_interval(p0, p1, p2, p3, t0, t1))


class SmoothChain:
    __slots__ = ('segments', 'cum_lengths', 'length')

    def __init__(self, segments):
        self.segments = segments
        cum = [0.0]
        for s in segments:
            cum.append(cum[-1] + s.length)
        self.cum_lengths = cum
        self.length = cum[-1]

    def start_tangent(self):
        return self.segments[0].start_tangent()

    def end_tangent(self):
        return self.segments[-1].end_tangent()

    def point_and_tangent_at_dist(self, d):
        d = max(0.0, min(self.length, d))
        for i, seg in enumerate(self.segments):
            s0 = self.cum_lengths[i]
            s1 = self.cum_lengths[i + 1]
            if d <= s1 or i == len(self.segments) - 1:
                return seg.point_and_tangent_at_dist(d - s0)
        return self.segments[-1].end, self.segments[-1].end_tangent()

    def trim(self, d_start, d_end):
        a = max(0.0, d_start)
        b = min(self.length, self.length - d_end)
        if b - a <= 0.25:
            return []
        out = []
        for i, seg in enumerate(self.segments):
            s0 = self.cum_lengths[i]
            s1 = self.cum_lengths[i + 1]
            ov0 = max(a, s0)
            ov1 = min(b, s1)
            if ov1 - ov0 > 0.25:
                sub = seg.subsegment_by_dist(ov0 - s0, ov1 - s0)
                if sub is not None:
                    out.append(sub)
        return out


def make_fillet_cubic(ptA, tanA, ptB, tanB, dA, dB):
    chord_dx = ptB[0] - ptA[0]
    chord_dy = ptB[1] - ptA[1]
    chord = math.hypot(chord_dx, chord_dy)
    if chord < 0.25:
        return None
    dot = max(-1.0, min(1.0, tanA[0] * tanB[0] + tanA[1] * tanB[1]))
    theta = math.acos(dot)
    tan_q = math.tan(theta / 4.0)
    kappa = (2.0 / 3.0) * max(0.25, 1.0 - tan_q * tan_q)
    hA = min(dA * kappa, chord * 0.72)
    hB = min(dB * kappa, chord * 0.72)
    c1 = (ptA[0] + tanA[0] * hA, ptA[1] + tanA[1] * hA)
    c2 = (ptB[0] - tanB[0] * hB, ptB[1] - tanB[1] * hB)
    return Segment('cubic', (ptA, c1, c2, ptB))


def ops_to_contours(ops):
    contours = []
    curr_segs = []
    curr_pt = None
    start_pt = None
    for op, args in ops:
        if op == 'moveTo':
            curr_pt = args[0]
            start_pt = args[0]
            curr_segs = []
        elif op == 'lineTo':
            nxt = args[0]
            if math.hypot(nxt[0] - curr_pt[0], nxt[1] - curr_pt[1]) > 1e-4:
                curr_segs.append(Segment('line', (curr_pt, nxt)))
                curr_pt = nxt
        elif op == 'curveTo':
            p1, p2, p3 = args
            curr_segs.append(Segment('cubic', (curr_pt, p1, p2, p3)))
            curr_pt = p3
        elif op == 'closePath':
            if curr_pt and start_pt and math.hypot(start_pt[0] - curr_pt[0], start_pt[1] - curr_pt[1]) > 1e-4:
                curr_segs.append(Segment('line', (curr_pt, start_pt)))
            if curr_segs:
                contours.append(curr_segs)
            curr_segs = []
    return contours


def get_stem_width(font):
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    p = RecordingPen()
    gs[cmap[ord('I')]].draw(p)
    segs = ops_to_contours(p.value)[0]
    lengths = sorted([s.length for s in segs])
    return float(lengths[0])


def round_contour(segs, stem_width, corner_angle_deg=18.0):
    n = len(segs)
    if n == 0:
        return segs
    corner_indices = []
    cos_thresh = math.cos(math.radians(corner_angle_deg))
    for i in range(n):
        t_in = segs[i - 1].end_tangent()
        t_out = segs[i].start_tangent()
        dot = t_in[0] * t_out[0] + t_in[1] * t_out[1]
        if dot < cos_thresh:
            corner_indices.append(i)
    if len(corner_indices) < 2:
        return segs

    k = len(corner_indices)
    chains = []
    for c_idx in range(k):
        start_seg = corner_indices[c_idx]
        end_seg = corner_indices[(c_idx + 1) % k]
        chain_segs = []
        idx = start_seg
        while True:
            chain_segs.append(segs[idx])
            idx = (idx + 1) % n
            if idx == end_seg:
                break
        chains.append(SmoothChain(chain_segs))

    angles = []
    crosses = []
    for i in range(k):
        t_in = chains[i - 1].end_tangent()
        t_out = chains[i].start_tangent()
        cross = t_in[0] * t_out[1] - t_in[1] * t_out[0]
        dot = max(-1.0, min(1.0, t_in[0] * t_out[0] + t_in[1] * t_out[1]))
        theta = math.acos(dot)
        angles.append(theta)
        crosses.append(cross)

    cap_radii = []
    is_cap_chain = [False] * k
    for i in range(k):
        nxt = (i + 1) % k
        L = chains[i].length
        if crosses[i] > 0 and crosses[nxt] > 0:
            tot_ang = math.degrees(angles[i] + angles[nxt])
            if 115.0 <= tot_ang <= 245.0 and L <= 1.65 * stem_width and L <= 1.05 * max(chains[i - 1].length, chains[nxt].length):
                is_cap_chain[i] = True
                t1 = math.tan(min(math.pi * 0.42, angles[i] / 2.0))
                t2 = math.tan(min(math.pi * 0.42, angles[nxt] / 2.0))
                R_cap = L / max(1e-6, t1 + t2)
                cap_radii.append(R_cap)

    local_R = 0.50 * stem_width
    if cap_radii:
        cap_radii_sorted = sorted(cap_radii)
        med_R = cap_radii_sorted[len(cap_radii_sorted) // 2]
        if med_R < local_R:
            local_R = max(0.18 * stem_width, med_R)

    R_convex = local_R
    R_concave = 0.28 * local_R

    d_in_req = [0.0] * k
    d_out_req = [0.0] * k
    for i in range(k):
        theta = angles[i]
        R = R_convex if crosses[i] > 0 else R_concave
        tan_half = math.tan(min(math.pi * 0.42, theta / 2.0))
        d = R * tan_half
        d_in_req[i] = d
        d_out_req[i] = d

    for i in range(k):
        if is_cap_chain[i]:
            nxt = (i + 1) % k
            L = chains[i].length
            t1 = math.tan(min(math.pi * 0.42, angles[i] / 2.0))
            t2 = math.tan(min(math.pi * 0.42, angles[nxt] / 2.0))
            R_cap = L / max(1e-6, t1 + t2)
            d1 = R_cap * t1
            d2 = R_cap * t2
            d_in_req[i] = d1
            d_out_req[i] = d1
            d_in_req[nxt] = d2
            d_out_req[nxt] = d2

    d_in = list(d_in_req)
    d_out = list(d_out_req)

    order = sorted(range(k), key=lambda idx: chains[idx].length)
    for i in order:
        nxt = (i + 1) % k
        L = chains[i].length
        need = d_out[i] + d_in[nxt]
        if need > L and need > 1e-6:
            if crosses[i] > 0 and crosses[nxt] < 0:
                d_in[nxt] = min(d_in[nxt], max(0.0, L - d_out[i]))
                if d_out[i] + d_in[nxt] > L:
                    d_out[i] = max(0.0, L - d_in[nxt])
                d_out[nxt] = min(d_out[nxt], d_in[nxt])
            elif crosses[i] < 0 and crosses[nxt] > 0:
                d_out[i] = min(d_out[i], max(0.0, L - d_in[nxt]))
                if d_out[i] + d_in[nxt] > L:
                    d_in[nxt] = max(0.0, L - d_out[i])
                d_in[i] = min(d_in[i], d_out[i])
            else:
                scale = L / need
                d_out[i] *= scale
                d_in[nxt] *= scale
                if crosses[i] < 0:
                    d_in[i] = min(d_in[i], d_out[i])
                if crosses[nxt] < 0:
                    d_out[nxt] = min(d_out[nxt], d_in[nxt])

    for i in range(k):
        if crosses[i] < 0:
            m = min(d_in[i], d_out[i])
            d_in[i] = m
            d_out[i] = m
        else:
            if d_in[i] > 2.2 * d_out[i]:
                d_in[i] = 2.2 * d_out[i]
            elif d_out[i] > 2.2 * d_in[i]:
                d_out[i] = 2.2 * d_in[i]

    new_segs = []
    for i in range(k):
        nxt = (i + 1) % k
        ptA, tanA = chains[i - 1].point_and_tangent_at_dist(chains[i - 1].length - d_in[i])
        ptB, tanB = chains[i].point_and_tangent_at_dist(d_out[i])
        fillet = make_fillet_cubic(ptA, tanA, ptB, tanB, d_in[i], d_out[i])
        if fillet is not None:
            new_segs.append(fillet)
        rem = chains[i].trim(d_out[i], d_in[nxt])
        if rem:
            if new_segs:
                rem[0].pts = (new_segs[-1].end,) + rem[0].pts[1:]
            new_segs.extend(rem)

    if new_segs:
        for i in range(len(new_segs)):
            nxt = (i + 1) % len(new_segs)
            if math.hypot(new_segs[i].end[0] - new_segs[nxt].start[0], new_segs[i].end[1] - new_segs[nxt].start[1]) > 0.01:
                new_segs[nxt].pts = (new_segs[i].end,) + new_segs[nxt].pts[1:]
    return new_segs


import os
import sys
import time
import zipfile
import shutil
import argparse
import multiprocessing as mp
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

STYLES = [
    # (style_suffix, weight_num, fstyle, is_italic, is_bold, is_ribbi, fs_selection)
    ("Thin", 100, "normal", False, False, False, 0x00c0),
    ("ThinItalic", 100, "italic", True, False, False, 0x0081),
    ("ExtraLight", 200, "normal", False, False, False, 0x00c0),
    ("ExtraLightItalic", 200, "italic", True, False, False, 0x0081),
    ("Light", 300, "normal", False, False, False, 0x00c0),
    ("LightItalic", 300, "italic", True, False, False, 0x0081),
    ("Regular", 400, "normal", False, False, True, 0x00c0),
    ("Italic", 400, "italic", True, False, True, 0x0081),
    ("Medium", 500, "normal", False, False, False, 0x00c0),
    ("MediumItalic", 500, "italic", True, False, False, 0x0081),
    ("SemiBold", 600, "normal", False, False, False, 0x00c0),
    ("SemiBoldItalic", 600, "italic", True, False, False, 0x0081),
    ("Bold", 700, "normal", False, True, True, 0x00a0),
    ("BoldItalic", 700, "italic", True, True, True, 0x00a1),
    ("ExtraBold", 800, "normal", False, False, False, 0x00c0),
    ("ExtraBoldItalic", 800, "italic", True, False, False, 0x0081),
    ("Black", 900, "normal", False, False, False, 0x00c0),
    ("BlackItalic", 900, "italic", True, False, False, 0x0081),
]


def update_font_names(font, style_suffix, weight_num, is_italic, is_bold, is_ribbi, fs_selection):
    # Update head
    font['head'].fontRevision = 1.000

    # Update name table
    for rec in font['name'].names:
        s = rec.toUnicode()
        if rec.nameID in (1, 3, 4, 6, 16):
            s_new = s.replace("Inter-", "CollabSans-")
            if s_new.startswith("Inter "):
                s_new = "Collab Sans " + s_new[len("Inter "):]
            elif s_new == "Inter":
                s_new = "Collab Sans"
            rec.string = s_new.encode(rec.getEncoding())
        elif rec.nameID in (0, 7, 8, 9, 11, 12):
            s_new = s.replace("<your-github-username>", "yugal")
            s_new = s_new.replace("<your-email@example.com>", "yugalone@users.noreply.github.com")
            if rec.nameID == 7:
                s_new = "Collab Sans is a trademark of Yugal."
            elif rec.nameID == 8:
                s_new = "Yugal"
            rec.string = s_new.encode(rec.getEncoding())

    # For RIBBI styles, omit redundant Typographic Family/Subfamily (NameID 16 & 17)
    if is_ribbi:
        font['name'].names = [rec for rec in font['name'].names if rec.nameID not in (16, 17)]
    else:
        has_16 = any(r.nameID == 16 for r in font['name'].names)
        if not has_16:
            subfamily = "Regular"
            for r in font['name'].names:
                if r.nameID == 2:
                    subfamily = r.toUnicode()
                    break
            font['name'].setName("Collab Sans", 16, 3, 1, 0x409)
            font['name'].setName(subfamily, 17, 3, 1, 0x409)

    # Set exact italicAngle and underline metrics
    if 'post' in font:
        font['post'].italicAngle = -9.4 if is_italic else 0.0
        font['post'].underlineThickness = 192
        font['post'].underlinePosition = -464

    # Set OS/2 properties
    if 'OS/2' in font:
        os2 = font['OS/2']
        os2.usWeightClass = weight_num
        os2.fsSelection = fs_selection
        os2.achVendID = 'COLB'
        os2.usWinAscent = 3180
        os2.usWinDescent = 928

    # Set hhea caret slope
    if 'hhea' in font:
        hhea = font['hhea']
        if is_italic:
            hhea.caretSlopeRise = 2816
            hhea.caretSlopeRun = 466
            hhea.caretOffset = 0
        else:
            hhea.caretSlopeRise = 1
            hhea.caretSlopeRun = 0
            hhea.caretOffset = 0

    # Update CFF names if present
    if 'CFF ' in font:
        cff = font['CFF '].cff
        cff.fontNames = [f"CollabSans-{style_suffix}"]
        td = cff.topDictIndex[0]
        if hasattr(td, 'FullName') and td.FullName:
            if td.FullName.startswith("Inter "):
                td.FullName = "Collab Sans " + td.FullName[len("Inter "):]
            elif td.FullName == "Inter":
                td.FullName = "Collab Sans"
        if hasattr(td, 'FamilyName') and td.FamilyName:
            if td.FamilyName.startswith("Inter "):
                td.FamilyName = "Collab Sans " + td.FamilyName[len("Inter "):]
            elif td.FamilyName == "Inter":
                td.FamilyName = "Collab Sans"
        if hasattr(td, 'Notice') and td.Notice:
            td.Notice = td.Notice.replace("<your-github-username>", "yugal")
        if hasattr(td, 'Copyright') and td.Copyright:
            td.Copyright = td.Copyright.replace("<your-github-username>", "yugal")


def convert_otf_to_ttf(otf_path, ttf_path):
    otf = TTFont(otf_path)
    gs = otf.getGlyphSet()
    glyphOrder = otf.getGlyphOrder()

    glyf = newTable('glyf')
    glyf.glyphs = {}
    glyf.glyphOrder = glyphOrder

    for gname in glyphOrder:
        ttpen = TTGlyphPen(None)
        cu2qu = Cu2QuPen(ttpen, max_err=1.5, reverse_direction=True)
        gs[gname].draw(cu2qu)
        glyf.glyphs[gname] = ttpen.glyph()

    del otf['CFF ']
    otf.sfntVersion = '\x00\x01\x00\x00'
    otf['loca'] = newTable('loca')
    otf['glyf'] = glyf
    otf['maxp'].tableVersion = 0x00010000
    otf['maxp'].maxZones = 1
    otf['maxp'].maxTwilightPoints = 0
    otf['maxp'].maxStorage = 0
    otf['maxp'].maxFunctionDefs = 0
    otf['maxp'].maxInstructionDefs = 0
    otf['maxp'].maxStackElements = 0
    otf['maxp'].maxSizeOfInstructions = 0
    otf['maxp'].maxComponentElements = 0
    otf['maxp'].maxComponentDepth = 0
    otf['post'].formatType = 2.0
    otf['post'].extraNames = []
    otf['post'].mapping = {}

    gasp = newTable('gasp')
    gasp.gaspRange = {0xFFFF: 0x000F}
    otf['gasp'] = gasp

    otf.save(ttf_path)


def build_single_style(args):
    style_tuple, src_dir, out_dir = args
    style_suffix, weight_num, fstyle, is_italic, is_bold, is_ribbi, fs_selection = style_tuple
    t0 = time.time()

    src_candidates = [
        os.path.join(src_dir, f"Inter-{style_suffix}.otf"),
        os.path.join(src_dir, "otf", f"Inter-{style_suffix}.otf"),
        f"/usr/share/fonts/opentype/inter/Inter-{style_suffix}.otf",
    ]
    src_path = None
    for cand in src_candidates:
        if os.path.exists(cand):
            src_path = cand
            break

    if not src_path:
        raise FileNotFoundError(f"Could not locate source font for Inter-{style_suffix}. Checked: {src_candidates}")

    font = TTFont(src_path)
    stem_w = get_stem_width(font)
    cff = font['CFF '].cff
    topDict = cff.topDictIndex[0]
    charStrings = topDict.CharStrings
    gs = font.getGlyphSet()

    for gname in font.getGlyphOrder():
        glyph = gs[gname]
        p = RecordingPen()
        glyph.draw(p)
        if not p.value:
            continue
        orig_contours = ops_to_contours(p.value)
        if not orig_contours:
            continue
        t2pen = T2CharStringPen(glyph.width, glyphSet=None)
        for c in orig_contours:
            rc = round_contour(c, stem_w)
            if not rc:
                continue
            t2pen.moveTo(rc[0].start)
            for s in rc:
                if s.kind == 'line':
                    t2pen.lineTo(s.end)
                else:
                    _, p1, p2, p3 = s.pts
                    t2pen.curveTo(p1, p2, p3)
            t2pen.closePath()
        charStrings[gname] = t2pen.getCharString(private=topDict.Private)

    update_font_names(font, style_suffix, weight_num, is_italic, is_bold, is_ribbi, fs_selection)

    otf_path = os.path.join(out_dir, "otf", f"CollabSans-{style_suffix}.otf")
    woff2_path = os.path.join(out_dir, "woff2", f"CollabSans-{style_suffix}.woff2")
    ttf_path = os.path.join(out_dir, "ttf", f"CollabSans-{style_suffix}.ttf")

    os.makedirs(os.path.dirname(otf_path), exist_ok=True)
    os.makedirs(os.path.dirname(woff2_path), exist_ok=True)
    os.makedirs(os.path.dirname(ttf_path), exist_ok=True)

    font.save(otf_path)

    # Save WOFF2
    font.flavor = 'woff2'
    font.save(woff2_path)

    # Convert to TTF
    convert_otf_to_ttf(otf_path, ttf_path)

    elapsed = time.time() - t0
    return f"Built CollabSans-{style_suffix} (OTF, TTF, WOFF2) in {elapsed:.1f}s"


def main():
    parser = argparse.ArgumentParser(description="Generate Collab Rounded Font Family from Inter")
    parser.add_argument("--src-dir", default="/usr/share/fonts/opentype/inter", help="Directory containing source Inter OTF files")
    parser.add_argument("--out-dir", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts")), help="Target output fonts directory")
    parser.add_argument("--processes", type=int, default=2, help="Number of parallel worker processes")
    args = parser.parse_args()

    t_start = time.time()
    for sub in ["otf", "ttf", "woff2"]:
        os.makedirs(os.path.join(args.out_dir, sub), exist_ok=True)

    work_items = [(style, args.src_dir, args.out_dir) for style in STYLES]

    with mp.Pool(processes=args.processes) as pool:
        for msg in pool.imap_unordered(build_single_style, work_items):
            print(msg, flush=True)

    print(f"\nAll Collab styles built successfully in {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
