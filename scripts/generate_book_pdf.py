import os
import sys
import asyncio
import re
import pymupdf  # PyMuPDF
from pyppeteer import launch

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HTML_SOURCE = os.path.join(WORKSPACE_DIR, "public", "_print", "book", "index.html")

SCRATCH_DIR = os.path.join(WORKSPACE_DIR, "scratch")
TITLE_HTML = os.path.join(SCRATCH_DIR, "title_pages.html")
TITLE_PDF = os.path.join(SCRATCH_DIR, "title_pages.pdf")
CONTENT_HTML = os.path.join(SCRATCH_DIR, "content_pages.html")
CONTENT_PDF = os.path.join(SCRATCH_DIR, "content_pages.pdf")

OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "static", "downloads", "Modern_Front_End_Engineering.pdf")
PUBLIC_PDF = os.path.join(WORKSPACE_DIR, "public", "downloads", "Modern_Front_End_Engineering.pdf")
FRONT_COVER_IMG = os.path.join(WORKSPACE_DIR, "images", "cover-front.png")
BACK_COVER_IMG = os.path.join(WORKSPACE_DIR, "images", "cover-back.png")
MAIN_CSS = os.path.join(WORKSPACE_DIR, "public", "scss", "main.css")
FA_CSS = os.path.join(WORKSPACE_DIR, "public", "scss", "fontawesome.css")

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_DIR, "static", "downloads"), exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_DIR, "public", "downloads"), exist_ok=True)


def get_base_css():
    main_css_content = ""
    fa_css_content = ""
    if os.path.exists(MAIN_CSS):
        with open(MAIN_CSS, "r", encoding="utf-8") as f:
            main_css_content = f.read()
    if os.path.exists(FA_CSS):
        with open(FA_CSS, "r", encoding="utf-8") as f:
            fa_css_content = f.read()

    # Strip out any counter(page) in @bottom-center to avoid duplicate page numbers
    main_css_content = re.sub(r'@bottom-center\s*\{[^}]*\}', '', main_css_content)

    custom_css = """
    * {
      box-sizing: border-box;
    }

    html, body {
      background: #ffffff !important;
      background-color: #ffffff !important;
      color: #0f172a !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
      font-size: 10pt !important;
      line-height: 1.65 !important;
      -webkit-font-smoothing: antialiased;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    .td-print-view {
      background: #ffffff !important;
    }

    .container-fluid, .td-print-shell, .td-print-document, main {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      border: none !important;
      box-shadow: none !important;
      background: #ffffff !important;
    }

    /* Table of Contents Styling */
    .td-book-print-cover {
      page-break-before: always;
      page-break-after: always;
      break-after: page;
      padding-top: 10px;
    }
    .td-book-print-cover h1.title {
      font-size: 26pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      border-bottom: 2pt solid #0284c7;
      padding-bottom: 12px;
      margin-bottom: 12px;
    }
    .td-book-print-cover .lead {
      font-size: 12pt !important;
      color: #475569 !important;
      margin-bottom: 24px !important;
    }
    .td-book-print-toc ol {
      list-style: none;
      padding-left: 0;
      margin: 0;
    }
    .td-book-print-toc li {
      padding: 6px 0;
      border-bottom: 0.5pt dotted #cbd5e1;
      font-size: 9.5pt;
      break-inside: avoid;
    }
    .td-book-print-toc a {
      color: #0369a1 !important;
      text-decoration: none;
    }
    .td-book-print-toc .td-book-number {
      font-weight: 700;
      color: #0f172a;
      display: inline-block;
      width: 28px;
    }

    /* Chapter and Section Headings */
    .td-book-print-page {
      page-break-before: always !important;
      break-before: page !important;
      padding-top: 16px !important;
    }
    .td-book-print-page h1 {
      font-size: 22pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      border-bottom: 1.5pt solid #0284c7 !important;
      padding-bottom: 10px !important;
      margin-top: 10px !important;
      margin-bottom: 14px !important;
      line-height: 1.25 !important;
    }
    .td-book-print-page .lead {
      font-size: 10.5pt !important;
      font-style: italic !important;
      color: #334155 !important;
      margin-bottom: 18px !important;
      background: #f8fafc;
      padding: 10px 14px;
      border-inline-start: 3pt solid #0284c7;
      border-radius: 4px;
    }
    h2 {
      font-size: 14pt !important;
      font-weight: 700 !important;
      color: #1e293b !important;
      margin-top: 22px !important;
      margin-bottom: 10px !important;
      border-bottom: 0.5pt solid #e2e8f0 !important;
      padding-bottom: 4px !important;
      break-after: avoid-page !important;
    }
    h3 {
      font-size: 11.5pt !important;
      font-weight: 600 !important;
      color: #334155 !important;
      margin-top: 16px !important;
      margin-bottom: 8px !important;
      break-after: avoid-page !important;
    }
    p {
      margin-bottom: 10px !important;
      text-align: justify;
      hyphens: auto;
    }

    /* Code Blocks */
    pre, .chroma, .highlight {
      background: #f8fafc !important;
      border: 0.75pt solid #cbd5e1 !important;
      border-radius: 4px !important;
      padding: 8px 12px !important;
      font-family: "Cascadia Code", Consolas, "Courier New", monospace !important;
      font-size: 8pt !important;
      line-height: 1.45 !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      break-inside: avoid-page !important;
      margin-bottom: 12px !important;
    }
    code {
      font-family: "Cascadia Code", Consolas, "Courier New", monospace !important;
      font-size: 8.5pt !important;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0f172a !important;
    }

    /* Callout & Notes */
    blockquote, .td-callout {
      background: #f0f9ff !important;
      border-inline-start: 3.5pt solid #0284c7 !important;
      padding: 10px 14px !important;
      margin: 14px 0 !important;
      border-radius: 0 4px 4px 0;
      break-inside: avoid-page !important;
      font-size: 9.5pt !important;
    }

    /* Tables */
    table, .td-table {
      width: 100% !important;
      border-collapse: collapse !important;
      margin: 14px 0 !important;
      font-size: 8.5pt !important;
      break-inside: avoid-page !important;
    }
    th {
      background: #f1f5f9 !important;
      color: #0f172a !important;
      font-weight: 700 !important;
      border: 0.5pt solid #cbd5e1 !important;
      padding: 6px 10px !important;
      text-align: left !important;
    }
    td {
      border: 0.5pt solid #cbd5e1 !important;
      padding: 6px 10px !important;
    }
    tr:nth-child(even) td {
      background: #f8fafc !important;
    }

    /* Figures & Images */
    figure, img {
      max-width: 100% !important;
      height: auto !important;
      break-inside: avoid-page !important;
    }
    figcaption {
      font-size: 8.5pt !important;
      color: #64748b !important;
      text-align: center;
      margin-top: 6px;
      font-style: italic;
    }

    /* Hide Navigation / Web UI Artifacts */
    .td-skip-link, .td-heading-self-link, .td-page-actions, .td-code__copy, .d-print-none, .td-book-cover-page {
      display: none !important;
    }
    """
    return f"""
    <style>
      {main_css_content}
      {fa_css_content}
      {custom_css}
    </style>
    """


def prepare_documents():
    print("Preparing Title & Colophon Document...")
    base_css = get_base_css()

    title_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Title & Colophon</title>
  {base_css}
  <style>
    @page {{
      size: A4;
      margin: 20mm 20mm 20mm 20mm;
    }}
    .formal-title-page {{
      page-break-after: always;
      break-after: page;
      min-height: 800px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-align: center;
      padding: 40px 10px;
    }}
    .formal-title-page h1 {{
      font-size: 32pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      margin-bottom: 12px !important;
      line-height: 1.2 !important;
    }}
    .colophon-page {{
      page-break-before: always;
      break-before: page;
      padding: 80px 20px 40px;
      font-size: 9pt;
      color: #475569;
      line-height: 1.7;
    }}
  </style>
</head>
<body style="background: #ffffff !important;">
  <div class="formal-title-page">
    <div>
      <div style="font-size: 11pt; text-transform: uppercase; letter-spacing: 0.15em; color: #64748b; margin-bottom: 30px; font-weight: 600;">Textbook and Engineering Monograph</div>
      <h1>Modern Front-End Engineering</h1>
      <div style="font-size: 15pt; color: #475569; font-style: italic; margin-bottom: 40px;">From Browser Fundamentals to Production Architecture</div>
    </div>

    <div style="margin: 40px auto;">
      <svg width="84" height="84" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
        <path d="M2 12h20"></path>
      </svg>
    </div>

    <div style="margin-top: auto; border-top: 1.5pt solid #cbd5e1; padding-top: 24px;">
      <div style="font-size: 16pt; font-weight: 700; color: #0f172a;">Dr. Polla Abdulhamid Fattah</div>
      <div style="font-size: 11pt; color: #64748b; margin-top: 4px;">and Collection of LLMs</div>
      <div style="font-size: 9.5pt; color: #64748b; margin-top: 12px; line-height: 1.5;">
        Senior Lecturer, Software &amp; Informatics Engineering, Salahaddin University-Erbil<br>
        Artificial Intelligence and Innovation Centre, University of Kurdistan Hewlêr<br>
        Software Development Team Manager, SmartGate
      </div>
      <div style="font-size: 8.5pt; color: #94a3b8; margin-top: 24px; text-transform: uppercase; letter-spacing: 0.1em;">
        First Edition - Academic &amp; Production Reference - 2026
      </div>
    </div>
  </div>

  <div class="colophon-page">
    <h3 style="font-size: 13pt; color: #0f172a; margin-bottom: 12px;">Modern Front-End Engineering</h3>
    <p style="font-style: italic; color: #64748b; margin-bottom: 20px;">From Browser Fundamentals to Production Architecture</p>

    <p><strong>Author:</strong> Dr. Polla Abdulhamid Fattah</p>
    <p><strong>Published By:</strong> Academic &amp; Professional Engineering Monograph Series</p>
    <p><strong>Publication Date:</strong> 2026</p>
    <p><strong>Repository &amp; Continuous Updates:</strong> <a href="https://github.com/polla-fattah/frontend-book" style="color: #0284c7;">github.com/polla-fattah/frontend-book</a></p>
    <p><strong>Online Interactive Platform:</strong> <a href="https://polla.dev/frontend-book/" style="color: #0284c7;">polla.dev/frontend-book/</a></p>

    <div style="margin-top: 36px; padding: 16px; background: #f8fafc; border-left: 3pt solid #0284c7; border-radius: 4px;">
      <p style="margin: 0; font-size: 8.5pt; color: #334155;">
        <strong>About This Work:</strong><br>
        This monograph presents front-end development as an engineering discipline, bridging raw computer science fundamentals (rendering engines, memory models, compilation pipelines, ASTs) with large-scale production architecture (micro-frontends, typed runtime boundaries, offline replication, Core Web Vitals, and observability). Designed for senior engineers, engineering leaders, and university students.
      </p>
    </div>

    <div style="margin-top: 50px; font-size: 8pt; color: #94a3b8; line-height: 1.6;">
      <p>Copyright &copy; 2026 Dr. Polla Abdulhamid Fattah. All rights reserved.</p>
      <p>No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form without prior written permission of the author, except for fair use in academic coursework, non-commercial education, and software development practices.</p>
    </div>
  </div>
</body>
</html>
"""
    with open(TITLE_HTML, "w", encoding="utf-8") as f:
        f.write(title_html)

    print("Preparing Content Pages Document...")
    with open(HTML_SOURCE, "r", encoding="utf-8") as f:
        content_raw = f.read()

    # Force html tag to pure light mode
    content_raw = re.sub(
        r'<html[^>]*>',
        '<html lang="en" data-bs-theme="light" data-theme="light" class="light-mode">',
        content_raw,
        count=1
    )

    # Strip theme switcher script so it doesn't dynamically flip to dark mode
    content_raw = re.sub(r'<script>\s*\(function\(\)\s*\{\s*const themeKey.*?</script>', '', content_raw, flags=re.DOTALL)

    # Set meta color-scheme to light
    content_raw = re.sub(r'<meta name="color-scheme"[^>]*>', '<meta name="color-scheme" content="light">', content_raw)

    # Remove only the inline dark-theme canvas override (keep all script tags so Mermaid runs)
    content_raw = re.sub(r'<style>\s*html\s*\{[^}]*Canvas.*?<\/style>', '', content_raw, flags=re.DOTALL)

    # Remove cover divs
    content_raw = re.sub(r'<div class="td-book-cover-page[^"]*".*?</div>', '', content_raw, flags=re.DOTALL)

    # Convert any mdash to hyphens
    content_raw = content_raw.replace("\u2014", " - ").replace("&mdash;", " - ")

    # Inject base CSS with explicit @page and root white background overrides
    page_white_css = """
    <style>
    @page {
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    html, :root {
      color-scheme: light !important;
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    body, .td-print-view, .container-fluid, .td-print-shell, .td-print-document, main {
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    </style>
    """
    content_raw = content_raw.replace("</head>", f"{base_css}\n{page_white_css}</head>")

    with open(CONTENT_HTML, "w", encoding="utf-8") as f:
        f.write(content_raw)

    print("Documents prepared.")


async def render_pdfs():
    print("Launching Chrome headless...")
    browser = await launch(
        executablePath=CHROME_PATH,
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-dev-shm-usage",
            "--force-color-profile=srgb",
            "--blink-settings=forceDarkModeEnabled=false",
        ],
    )
    page = await browser.newPage()

    # Enforce light color scheme via Chrome DevTools Protocol
    try:
        await page._client.send('Emulation.setEmulatedMedia', {
            'media': 'screen',
            'features': [{'name': 'prefers-color-scheme', 'value': 'light'}]
        })
    except Exception as e:
        print(f"Notice: setEmulatedMedia: {e}")

    await page.emulateMedia('screen')

    # 1. Render Title and Colophon (NO headers, NO footers)
    print("Rendering Title and Colophon to PDF...")
    title_url = f"file:///{TITLE_HTML.replace('\\', '/')}"
    await page.goto(title_url, {"waitUntil": "networkidle0", "timeout": 60000})
    await page.pdf({
        "path": TITLE_PDF,
        "format": "A4",
        "printBackground": True,
        "displayHeaderFooter": False,
        "margin": {
            "top": "20mm",
            "bottom": "20mm",
            "left": "20mm",
            "right": "20mm",
        },
    })

    # 2. Render Content (WITH elegant running headers and footers)
    print("Rendering Content to PDF...")
    content_url = f"file:///{CONTENT_HTML.replace('\\', '/')}"
    await page.goto(content_url, {"waitUntil": "networkidle0", "timeout": 120000})

    # Wait for Mermaid diagrams to render (they produce SVG inside .td-diagram--mermaid)
    print("Waiting for Mermaid diagrams to render...")
    try:
        await page.waitForFunction(
            """
            () => {
                const containers = document.querySelectorAll('.td-diagram--mermaid');
                if (containers.length === 0) return true;  // no diagrams, proceed
                return Array.from(containers).every(el => el.querySelector('svg') !== null);
            }
            """,
            {"timeout": 60000, "polling": 500}
        )
        print("Mermaid diagrams rendered.")
    except Exception as e:
        print(f"Warning: Mermaid wait timed out or errored ({e}). Proceeding anyway.")

    # Extra settle time for fonts and layout reflow
    await asyncio.sleep(2)

    header_template = """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 7.5pt; color: #64748b; width: 100%; padding: 0 20mm; display: flex; justify-content: space-between; border-bottom: 0.5pt solid #cbd5e1; padding-bottom: 3px;">
      <span>Modern Front-End Engineering</span>
      <span>Dr. Polla Abdulhamid Fattah</span>
    </div>
    """

    footer_template = """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 7.5pt; color: #64748b; width: 100%; padding: 0 20mm; display: flex; justify-content: space-between; border-top: 0.5pt solid #cbd5e1; padding-top: 3px;">
      <span>Salahaddin University-Erbil &bull; UKH AIIC</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    """

    await page.pdf({
        "path": CONTENT_PDF,
        "format": "A4",
        "printBackground": True,
        "displayHeaderFooter": True,
        "headerTemplate": header_template,
        "footerTemplate": footer_template,
        "margin": {
            "top": "22mm",
            "bottom": "22mm",
            "left": "20mm",
            "right": "20mm",
        },
    })

    await browser.close()
    print("Both PDF parts rendered.")


def assemble_final_pdf():
    print("Assembling final publication PDF with PyMuPDF...")
    A4_WIDTH = 595.276
    A4_HEIGHT = 841.890
    a4_rect = pymupdf.Rect(0, 0, A4_WIDTH, A4_HEIGHT)
    bg_color = (13 / 255.0, 20 / 255.0, 28 / 255.0)

    def add_cover(document, image_path):
        page = document.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        page.draw_rect(a4_rect, color=bg_color, fill=bg_color, overlay=True)
        page.insert_image(a4_rect, filename=image_path, keep_proportion=False)
        return page

    final_doc = pymupdf.open()

    # 1. Front Cover (Full Bleed)
    print(f"Adding Front Cover from {FRONT_COVER_IMG}...")
    add_cover(final_doc, FRONT_COVER_IMG)

    # 2. Title & Colophon Pages (2 pages, clean)
    print(f"Inserting Title & Colophon pages ({TITLE_PDF})...")
    title_doc = pymupdf.open(TITLE_PDF)
    final_doc.insert_pdf(title_doc)
    title_doc.close()

    # 3. Main Content Pages (TOC + Chapters 1-18 + Appendices A-C)
    print(f"Inserting Book Content pages ({CONTENT_PDF})...")
    content_doc = pymupdf.open(CONTENT_PDF)
    final_doc.insert_pdf(content_doc)
    content_doc.close()

    # 4. Back Cover (Full Bleed)
    print(f"Adding Back Cover from {BACK_COVER_IMG}...")
    add_cover(final_doc, BACK_COVER_IMG)

    # Save
    final_doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    final_doc.save(PUBLIC_PDF, garbage=4, deflate=True)
    page_count = len(final_doc)
    final_doc.close()

    file_size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print("=" * 60)
    print(f"SUCCESS! Publication-grade PDF assembled successfully!")
    print(f"Path: {OUTPUT_PDF}")
    print(f"Total Pages: {page_count}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    prepare_documents()
    asyncio.get_event_loop().run_until_complete(render_pdfs())
    assemble_final_pdf()
