from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from resume_data import (
    NAME, TITLE, LOCATION, EMAIL_USER, EMAIL_DOMAIN,
    SUMMARY, SKILLS, EDUCATION,
    EXPERIENCE_SECTION_LABEL, BOLD_TERMS, JOBS,
    RECOGNITIONS, PATENT_LINE, PATENT_DESCRIPTION,
)
from reportlab.pdfgen import canvas

WIDTH, HEIGHT = letter
SIDEBAR_W = 2.4 * inch
MARGIN = 0.38 * inch

THEMES = [
    {
        "filename": "Resume_Navy_White.pdf",
        "sb_bg": "#1C2E4A",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#A8C4E0",
        "sb_heading": "#4A90D9",
        "sb_label": "#A8C4E0",
        "sb_value": "#D4E4F0",
        "sb_divider": "#2D4A6A",
        "main_bg": "#FFFFFF",
        "main_text": "#1C2E4A",
        "main_light": "#5F7A96",
        "main_heading": "#4A90D9",
        "main_divider": "#D0DCE8",
        "bullet_dot": "#4A90D9",
    },
    {
        "filename": "Resume_Slate_Light.pdf",
        "sb_bg": "#2D3748",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#A0AEC0",
        "sb_heading": "#63B3ED",
        "sb_label": "#A0AEC0",
        "sb_value": "#CBD5E0",
        "sb_divider": "#4A5568",
        "main_bg": "#F7FAFC",
        "main_text": "#2D3748",
        "main_light": "#718096",
        "main_heading": "#63B3ED",
        "main_divider": "#E2E8F0",
        "bullet_dot": "#63B3ED",
    },
    {
        "filename": "Resume_Charcoal_Warm.pdf",
        "sb_bg": "#2C3E50",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#BDC3C7",
        "sb_heading": "#E67E22",
        "sb_label": "#BDC3C7",
        "sb_value": "#D5DBDB",
        "sb_divider": "#3D5166",
        "main_bg": "#FAFAFA",
        "main_text": "#2C3E50",
        "main_light": "#7F8C8D",
        "main_heading": "#E67E22",
        "main_divider": "#E5E5E5",
        "bullet_dot": "#E67E22",
    },
    {
        "filename": "Resume_Teal_Offwhite.pdf",
        "sb_bg": "#1A3C4A",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#9ECFDF",
        "sb_heading": "#5BA8BE",
        "sb_label": "#9ECFDF",
        "sb_value": "#C8E4EE",
        "sb_divider": "#2A5C70",
        "main_bg": "#F8F8F6",
        "main_text": "#1A3C4A",
        "main_light": "#4A7A8A",
        "main_heading": "#5BA8BE",
        "main_divider": "#D8EAF0",
        "bullet_dot": "#5BA8BE",
    },
    # --- Gray palettes ---
    {
        "filename": "Resume_Carbon_White.pdf",
        "sb_bg": "#2E2E2E",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#AAAAAA",
        "sb_heading": "#CCCCCC",
        "sb_label": "#AAAAAA",
        "sb_value": "#CCCCCC",
        "sb_divider": "#444444",
        "main_bg": "#FFFFFF",
        "main_text": "#1A1A1A",
        "main_light": "#666666",
        "main_heading": "#333333",
        "main_divider": "#E0E0E0",
        "bullet_dot": "#888888",
    },
    {
        "filename": "Resume_Graphite_Light.pdf",
        "sb_bg": "#3B3B3B",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#B0B0B0",
        "sb_heading": "#9FA9AD",
        "sb_label": "#B0B0B0",
        "sb_value": "#CCCCCC",
        "sb_divider": "#4F4F4F",
        "main_bg": "#F4F4F4",
        "main_text": "#2A2A2A",
        "main_light": "#777777",
        "main_heading": "#555555",
        "main_divider": "#DEDEDE",
        "bullet_dot": "#9FA9AD",
    },
    {
        "filename": "Resume_BlueGray_OffWhite.pdf",
        "sb_bg": "#3D4F5C",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#A8BBC6",
        "sb_heading": "#8AAABB",
        "sb_label": "#A8BBC6",
        "sb_value": "#C8D8E0",
        "sb_divider": "#4F6370",
        "main_bg": "#FAF9F6",
        "main_text": "#2C3740",
        "main_light": "#6B8090",
        "main_heading": "#3D4F5C",
        "main_divider": "#DDE5EA",
        "bullet_dot": "#8AAABB",
    },
    {
        "filename": "Resume_WarmGray_Eggshell.pdf",
        "sb_bg": "#52484A",
        "sb_name": "#FFFFFF",
        "sb_subtitle": "#C2B9AC",
        "sb_heading": "#C2B9AC",
        "sb_label": "#C2B9AC",
        "sb_value": "#D5CEC8",
        "sb_divider": "#665A5C",
        "main_bg": "#F0EAD6",
        "main_text": "#2C2420",
        "main_light": "#7A6860",
        "main_heading": "#52484A",
        "main_divider": "#DDD5C5",
        "bullet_dot": "#8C7B6E",
    },
]


def wrap_text(c, text, font, size, max_width):
    lines = []
    words = text.split()
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        if c.stringWidth(test, font, size) > max_width:
            lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def draw_text_block(
    c, x, y, text, size, color, max_width, font="Helvetica", leading=None
):
    if leading is None:
        leading = size + 2
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap_text(c, text, font, size, max_width)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def draw_sidebar_heading(c, x, y, text, w, text_color, divider_color):
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(text_color)
    c.drawString(x, y, text.upper())
    y -= 5
    c.setStrokeColor(divider_color)
    c.setLineWidth(0.4)
    c.line(x, y, x + w, y)
    return y - 10


def draw_main_heading(c, x, y, text, w, text_color, divider_color):
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(text_color)
    c.drawString(x, y, text.upper())
    y -= 5
    c.setStrokeColor(divider_color)
    c.setLineWidth(0.4)
    c.line(x, y, x + w, y)
    return y - 9


def draw_bullet(c, x, y, text, size, color, max_width, bullet_color, bold_phrases=None):
    c.setFillColor(bullet_color)
    c.circle(x + 2, y + 2.5, 1.2, fill=1, stroke=0)
    bx = x + 9
    avail = max_width - 9
    font = "Helvetica"

    if bold_phrases:
        lines = wrap_text(c, text, font, size, avail)
        for i, line in enumerate(lines):
            cx = bx
            ly = y - i * (size + 2.5)
            remaining = line
            while remaining:
                found_bp = None
                bp_pos = len(remaining)
                for bp in bold_phrases:
                    idx = remaining.find(bp)
                    if idx != -1 and idx < bp_pos:
                        bp_pos = idx
                        found_bp = bp
                if found_bp is None:
                    c.setFont("Helvetica", size)
                    c.setFillColor(color)
                    c.drawString(cx, ly, remaining)
                    break
                else:
                    before = remaining[:bp_pos]
                    if before:
                        c.setFont("Helvetica", size)
                        c.setFillColor(color)
                        c.drawString(cx, ly, before)
                        cx += c.stringWidth(before, "Helvetica", size)
                    c.setFont("Helvetica-Bold", size)
                    c.setFillColor(color)
                    c.drawString(cx, ly, found_bp)
                    cx += c.stringWidth(found_bp, "Helvetica-Bold", size)
                    remaining = remaining[bp_pos + len(found_bp) :]
                    continue
                break
        return y - len(lines) * (size + 2.5)
    else:
        lines = wrap_text(c, text, font, size, avail)
        for i, line in enumerate(lines):
            c.setFont(font, size)
            c.setFillColor(color)
            c.drawString(bx, y - i * (size + 2.5), line)
        return y - len(lines) * (size + 2.5)


def generate(theme):
    t = {
        k: HexColor(v) if isinstance(v, str) and v.startswith("#") else v
        for k, v in theme.items()
    }

    c = canvas.Canvas(theme["filename"], pagesize=letter)

    # Backgrounds
    c.setFillColor(t["sb_bg"])
    c.rect(0, 0, SIDEBAR_W, HEIGHT, fill=1, stroke=0)
    c.setFillColor(t["main_bg"])
    c.rect(SIDEBAR_W, 0, WIDTH - SIDEBAR_W, HEIGHT, fill=1, stroke=0)

    # === SIDEBAR ===
    sx = MARGIN - 0.05 * inch
    sw = SIDEBAR_W - MARGIN * 1.5
    sy = HEIGHT - MARGIN - 0.1 * inch

    # Name
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(t["sb_name"])
    c.drawString(sx, sy, NAME)
    sy -= 14
    c.setFont("Helvetica", 8.5)
    c.setFillColor(t["sb_subtitle"])
    c.drawString(sx, sy, TITLE)
    sy -= 22

    # Contact
    sy = draw_sidebar_heading(
        c, sx, sy, "Contact", sw, t["sb_heading"], t["sb_divider"]
    )
    sy = draw_text_block(c, sx, sy, LOCATION, 8.5, t["sb_value"], sw)
    sy = draw_text_block(c, sx, sy, EMAIL_USER, 8.5, t["sb_value"], sw)
    sy = draw_text_block(c, sx, sy, EMAIL_DOMAIN, 8.5, t["sb_value"], sw)
    sy -= 10

    # Skills
    sy = draw_sidebar_heading(c, sx, sy, "Skills", sw, t["sb_heading"], t["sb_divider"])
    for label, value in SKILLS:
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(t["sb_label"])
        c.drawString(sx, sy, label)
        sy -= 10
        sy = draw_text_block(c, sx, sy, value, 8.5, t["sb_value"], sw)
        sy -= 4
    sy -= 6

    # Education
    sy = draw_sidebar_heading(
        c, sx, sy, "Education", sw, t["sb_heading"], t["sb_divider"]
    )
    for i, (degree, institution) in enumerate(EDUCATION):
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(t["sb_name"])
        c.drawString(sx, sy, degree)
        sy -= 10
        c.setFont("Helvetica", 8)
        c.setFillColor(t["sb_subtitle"])
        c.drawString(sx, sy, institution)
        if i < len(EDUCATION) - 1:
            sy -= 13

    # === MAIN ===
    mx = SIDEBAR_W + 0.3 * inch
    mw = WIDTH - mx - MARGIN
    my = HEIGHT - MARGIN - 0.1 * inch

    # Summary
    my = draw_text_block(c, mx, my, SUMMARY, 9, t["main_text"], mw)
    my -= 4
    c.setStrokeColor(t["main_divider"])
    c.setLineWidth(0.4)
    c.line(mx, my, mx + mw, my)
    my -= 10

    # Experience
    my = draw_main_heading(
        c, mx, my, EXPERIENCE_SECTION_LABEL, mw, t["main_heading"], t["main_divider"]
    )

    for i, job in enumerate(JOBS):
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(t["main_heading"])
        c.drawString(mx, my, job["team"])
        c.setFont("Helvetica", 8)
        c.setFillColor(t["main_light"])
        c.drawRightString(mx + mw, my, job["date"])
        my -= 10
        c.setFont("Helvetica", 8)
        c.setFillColor(t["main_light"])
        c.drawString(mx, my, job["title"])
        my -= 10

        for bullet in job["bullets"]:
            my = draw_bullet(
                c,
                mx,
                my,
                bullet,
                8.5,
                t["main_text"],
                mw,
                t["bullet_dot"],
                bold_phrases=BOLD_TERMS,
            )
            my -= 1

        my -= 2
        if i < len(jobs) - 1:
            c.setStrokeColor(t["main_divider"])
            c.setLineWidth(0.3)
            c.line(mx, my, mx + mw, my)
            my -= 7

    # Recognition
    my -= 2
    my = draw_main_heading(
        c, mx, my, "Recognition", mw, t["main_heading"], t["main_divider"]
    )

    half_w = mw / 2
    for left, right in RECOGNITIONS:
        c.setFillColor(t["bullet_dot"])
        c.circle(mx + 2, my + 2.5, 1.2, fill=1, stroke=0)
        c.setFont("Helvetica", 8)
        c.setFillColor(t["main_text"])
        c.drawString(mx + 8, my, left)

        rx = mx + half_w
        c.setFillColor(t["bullet_dot"])
        c.circle(rx + 2, my + 2.5, 1.2, fill=1, stroke=0)
        c.setFillColor(t["main_text"])
        c.drawString(rx + 8, my, right)
        my -= 11

    my -= 2
    c.setFont("Helvetica", 7)
    c.setFillColor(t["main_light"])
    c.drawString(mx, my, PATENT_LINE)
    my -= 9
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(mx, my, PATENT_DESCRIPTION)

    c.save()
    return theme["filename"]


for theme in THEMES:
    path = generate(theme)
    print(f"Saved: {path}")
