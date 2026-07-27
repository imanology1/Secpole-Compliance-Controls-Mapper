"""Excel coverage-report generator.

Produces a formatted .xlsx with:
  - a Summary sheet: an NxN coverage matrix across the requested frameworks
    (plain and weighted coverage), and per-framework control counts
  - one detail sheet per ordered framework pair listing every mapped control
    and every gap

Values are written directly (no in-sheet formulas), so no LibreOffice recalc
pass is required.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(name="Arial", bold=True, size=14)
BODY_FONT = Font(name="Arial", size=10)
GAP_FILL = PatternFill("solid", fgColor="FCE4E4")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _style_header(ws, row, ncols):
    for col in range(1, ncols + 1):
        c = ws.cell(row=row, column=col)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = BORDER


def _autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _pct_color(pct):
    if pct >= 66:
        return PatternFill("solid", fgColor="C6EFCE")
    if pct >= 33:
        return PatternFill("solid", fgColor="FFEB9C")
    return PatternFill("solid", fgColor="FFC7CE")


def build_report(mapper, frameworks, output_path):
    for fw in frameworks:
        mapper._require_framework(fw)

    wb = Workbook()

    # ---- Summary sheet ----
    ws = wb.active
    ws.title = "Summary"
    ws["A1"] = "Secpol Cross-Framework Coverage Report"
    ws["A1"].font = TITLE_FONT
    ws["A3"] = "Coverage matrix (row framework covered BY column framework)"
    ws["A3"].font = Font(name="Arial", bold=True, size=11)

    # matrix header
    start = 4
    ws.cell(row=start, column=1, value="Source \\ Target")
    for j, fw in enumerate(frameworks, start=2):
        ws.cell(row=start, column=j, value=fw)
    _style_header(ws, start, len(frameworks) + 1)

    for i, src in enumerate(frameworks, start=1):
        r = start + i
        cell = ws.cell(row=r, column=1, value=src)
        cell.font = Font(name="Arial", bold=True, size=10)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        for j, tgt in enumerate(frameworks, start=2):
            if src == tgt:
                ws.cell(row=r, column=j, value="—").alignment = Alignment(horizontal="center")
                continue
            cov = mapper.get_coverage(src, tgt)
            pct = cov["coverage_percent"]
            c = ws.cell(row=r, column=j, value=pct / 100.0)
            c.number_format = "0.0%"
            c.fill = _pct_color(pct)
            c.alignment = Alignment(horizontal="center")
            c.border = BORDER

    # per-framework control counts
    cnt_row = start + len(frameworks) + 3
    ws.cell(row=cnt_row, column=1, value="Framework")
    ws.cell(row=cnt_row, column=2, value="Known Controls")
    ws.cell(row=cnt_row, column=3, value="Locally Defined")
    _style_header(ws, cnt_row, 3)
    for k, fw in enumerate(frameworks, start=1):
        r = cnt_row + k
        ws.cell(row=r, column=1, value=fw).font = BODY_FONT
        ws.cell(row=r, column=2, value=len(mapper.ids_by_framework[fw])).font = BODY_FONT
        ws.cell(row=r, column=3,
                value=len(mapper.defined_ids_by_framework[fw])).font = BODY_FONT

    _autosize(ws, [22] + [14] * max(len(frameworks), 2))

    # ---- Detail sheets per ordered pair ----
    for src in frameworks:
        for tgt in frameworks:
            if src == tgt:
                continue
            _pair_sheet(wb, mapper, src, tgt)

    wb.save(output_path)
    return output_path


def _safe_sheet_name(name):
    for ch in r'[]:*?/\\':
        name = name.replace(ch, "-")
    return name[:31]


def _pair_sheet(wb, mapper, src, tgt):
    title = _safe_sheet_name(f"{src}_to_{tgt}")
    ws = wb.create_sheet(title=title)

    ws["A1"] = f"{src}  →  {tgt}"
    ws["A1"].font = TITLE_FONT
    cov = mapper.get_coverage(src, tgt)
    ws["A2"] = (f"Coverage {cov['coverage_percent']}%  |  "
                f"Weighted {cov['weighted_coverage_percent']}%  |  "
                f"{cov['mapped_controls']}/{cov['total_controls']} controls mapped")
    ws["A2"].font = Font(name="Arial", italic=True, size=10)

    headers = ["Source ID", "Source Name", "Target ID", "Target Name", "Relationship"]
    hrow = 4
    for j, h in enumerate(headers, start=1):
        ws.cell(row=hrow, column=j, value=h)
    _style_header(ws, hrow, len(headers))

    row = hrow + 1
    mapped = mapper.map_framework(src, tgt)
    for control, pairs in mapped:
        for m, target in pairs:
            ws.cell(row=row, column=1, value=control.id).font = BODY_FONT
            ws.cell(row=row, column=2, value=control.name).font = BODY_FONT
            ws.cell(row=row, column=3, value=target.id).font = BODY_FONT
            ws.cell(row=row, column=4, value=target.name).font = BODY_FONT
            ws.cell(row=row, column=5, value=m.relationship).font = BODY_FONT
            row += 1

    # gaps section
    row += 1
    ws.cell(row=row, column=1, value=f"GAPS — {src} controls with no {tgt} mapping")
    ws.cell(row=row, column=1).font = Font(name="Arial", bold=True, size=11, color="9C0006")
    row += 1
    ws.cell(row=row, column=1, value="Control ID")
    ws.cell(row=row, column=2, value="Name")
    _style_header(ws, row, 2)
    row += 1
    for g in mapper.get_gaps(src, tgt):
        ws.cell(row=row, column=1, value=g["id"]).font = BODY_FONT
        ws.cell(row=row, column=2, value=g["name"]).font = BODY_FONT
        ws.cell(row=row, column=1).fill = GAP_FILL
        ws.cell(row=row, column=2).fill = GAP_FILL
        row += 1

    _autosize(ws, [16, 42, 16, 42, 14])
