# tools/pdf_reader.py
import pdfplumber
import requests
import os

def read_pdf_from_url(url, max_length=3000):
    """
    下载 PDF 并提取文本（安全版）。
    
    参数：
    - url: PDF 文件 URL
    - max_length: 返回文本最大长度，避免内存过大
    
    返回：
    - PDF 文本内容（字符串） 或 None（无法读取）
    """
    temp_path = "temp.pdf"
    
    try:
        # 下载文件
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            print(f"[警告] 下载失败，状态码: {response.status_code}")
            return None
        
        # 检查是否是 PDF
        if "application/pdf" not in response.headers.get("Content-Type", ""):
            print(f"[警告] URL 不是 PDF 文件: {url}")
            return None
        
        # 写入临时文件
        with open(temp_path, "wb") as f:
            f.write(response.content)
        
        # 打开 PDF 并提取文本
        text = ""
        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        return text[:max_length]
    
    except Exception as e:
        print(f"[警告] 读取 PDF 失败: {e}")
        return None
    
    finally:
        # 删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)