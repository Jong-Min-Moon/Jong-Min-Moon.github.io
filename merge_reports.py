
import os
import re
import markdown
from fpdf import FPDF

# List of files in order
files = [
    "_posts/ise-547/2026-02-16-vibe-coding-report-1.md",
    "_posts/ise-547/2026-02-16-vibe-coding-report-2.md",
    "_posts/ise-547/2026-02-16-vibe-coding-report-3.md",
    "_posts/ise-547/2026-02-16-vibe-coding-report-4.md",
    "_posts/ise-547/2026-02-16-vibe-coding-report-5.md"
]

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Vibe Coding Reports', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def parse_with_frontmatter(content):
    title = "Untitled"
    body = content
    # Extract YAML frontmatter
    match = re.search(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        fm = match.group(1)
        body = match.group(2)
        # Extract title from frontmatter
        t_match = re.search(r"^title:\s*(?:\"(.*?)\"|'(.*?)'|(.*?))\s*$", fm, re.MULTILINE)
        if t_match:
            # group 1, 2, or 3 will be not None
            title = next(g for g in t_match.groups() if g is not None)
    return title, body

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("helvetica", size=12)

for filepath in files:
    full_path = os.path.abspath(filepath)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    title, body = parse_with_frontmatter(content)
    
    # Sanitize content for simple PDF font
    replacements = {
        '“': '"', '”': '"', 
        '‘': "'", '’': "'",
        '—': '--', '–': '-',
        '…': '...', '→': '->',
        '←': '<-'
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
        title = title.replace(old, new)

    # Convert markdown to html
    html = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    
    pdf.add_page()
    
    # Add Title
    pdf.set_font('helvetica', 'B', 16)
    pdf.multi_cell(0, 10, title, align='L')
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 12)
    
    # Write HTML
    try:
        pdf.write_html(html)
    except Exception as e:
        print(f"Error writing HTML for {filepath}: {e}")
        # Fallback to plain text if HTML fails?
        # Or just log it.

output_file = "vibe_coding_reports_merged.pdf"
pdf.output(output_file)
print(f"Created {output_file}")
