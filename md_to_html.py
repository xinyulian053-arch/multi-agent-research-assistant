# md_to_html.py
import markdown
import os

# 修改成你实际的文件路径（用 r'...' 防止反斜杠问题）
md_path = r"D:\multi-agent-research-assistant\quantum_computing_report.md"
html_path = r"D:\multi-agent-research-assistant\quantum_computing_report.html"

try:
    # 检查 Markdown 文件是否存在
    if not os.path.exists(md_path):
        print(f"错误：找不到 Markdown 文件 → {md_path}")
        exit(1)

    # 读取 .md 文件
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    print(f"成功读取 Markdown 文件，大小：{len(md_text):,} 字符")

    # 转成 HTML（加了常用扩展，支持表格、代码块等）
    html_text = markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'codehilite']
    )

    # 包成完整 HTML 页面
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Quantum Computing Report</title>
    <!-- 可选：加点简单样式，让看起来更好 -->
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; margin: 40px; max-width: 900px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ font-family: Consolas, monospace; }}
    </style>
</head>
<body>
    {html_text}
</body>
</html>"""

    # 写入 .html 文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"转换成功！HTML 文件已生成：\n{html_path}")
    print("接下来可以用 wkhtmltopdf 转换它为 PDF 了。")

except Exception as e:
    print(f"转换失败：{e}")