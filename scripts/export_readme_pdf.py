from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib import colors
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUT = ROOT / "docs" / "exports"
OUT.mkdir(parents=True, exist_ok=True)

def md_to_html(md_text: str) -> str:
    # Minimal Markdown → HTML converter for headings & code fences
    html = md_text
    html = re.sub(r'^# (.*)$', r'<para spaceBefore="12"><b><font size=16>\1</font></b></para>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)$', r'<para spaceBefore="10"><b><font size=14>\1</font></b></para>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*)$', r'<para spaceBefore="8"><b><font size=12>\1</font></b></para>', html, flags=re.MULTILINE)
    # code fences → monospaced paragraphs (simple)
    html = re.sub(r'```(.*?)```', lambda m: f'<para fontName="Courier">{m.group(1)}</para>', html, flags=re.DOTALL)
    html = html.replace('\n\n', '<br/><br/>')
    return html

def main():
    pdf_file = OUT / "S1_Batch_Pipeline.pdf"
    doc = SimpleDocTemplate(str(pdf_file), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    title = "<para align='center'><b><font size=18>Sentinel‑1 Batch Processing Pipeline</font></b></para>"
    story += [Paragraph(title, styles["Normal"]), Spacer(1, 12)]

    if README.exists():
        md = README.read_text(encoding="utf-8")
        html = md_to_html(md)
        story += [Paragraph(html, styles["Normal"])]

    story.append(PageBreak())
    story += [Paragraph("<b>Appendix</b>", styles["Title"])]
    story += [Paragraph("This document was auto-generated from README.md and local assets.", styles["Normal"])]

    doc.build(story)
    print("[PDF] written →", pdf_file)

if __name__ == "__main__":
    main()