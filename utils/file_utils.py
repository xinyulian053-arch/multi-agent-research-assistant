# utils/file_utils.py （完整最终版，推荐使用这个）
import os
import markdown
from playwright.sync_api import sync_playwright

def save_report(report, topic):
    """
    保存报告为 Markdown 文件
    """
    filename = f"{topic.replace(' ', '_')}_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Markdown report saved as {filename}")

def save_pdf(report, topic):
    """
    直接从 report 字符串生成 PDF（不再读取 .md 文件）
    Markdown → HTML → Playwright PDF
    """
    pdf_filename = f"{topic.replace(' ', '_')}_report.pdf"
    html_filename = f"{topic.replace(' ', '_')}_report_temp.html"  # 临时文件

    try:
        # Markdown → HTML
        html_content = markdown.markdown(
            report,
            extensions=['extra', 'tables', 'fenced_code', 'codehilite', 'mdx_math']
        )

        # 完整 HTML + 样式
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{topic} Report</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        h1, h2, h3 {{ color: #111; }}
        pre {{ 
            background: #f6f8fa; 
            padding: 16px; 
            border-radius: 6px; 
            overflow-x: auto; 
            font-size: 0.95em;
        }}
        code {{ font-family: Consolas, "Courier New", monospace; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f2f2f2; }}
        img {{ max-width: 100%; height: auto; }}
        ul, ol {{ padding-left: 20px; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(full_html)

        # Playwright 生成 PDF
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            file_url = f"file:///{os.path.abspath(html_filename).replace(os.sep, '/')}"
            page.goto(file_url, wait_until="networkidle")
            page.wait_for_timeout(1500)  # 确保渲染完成

            page.pdf(
                path=pdf_filename,
                format="A4",
                print_background=True,
                margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
                scale=1.0,
                prefer_css_page_size=True
            )
            browser.close()

        print(f"PDF report saved as {pdf_filename}")

    except Exception as e:
        print(f"生成 PDF 失败: {e}")
        raise

    finally:
        # 清理临时 HTML
        if os.path.exists(html_filename):
            os.remove(html_filename)