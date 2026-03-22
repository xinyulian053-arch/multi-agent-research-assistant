# writer_agent.py
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    api_key="sk-c9621c51ed704a9daf3309217ea0f046",  # 替换为你的 Key
    model="deepseek-chat",                          # 必填
    model_kwargs={}                                  # 可选
)

def write_report(summary, topic, references=None):
    # 原有逻辑
    prompt = f"Write a structured research report about '{topic}' based on this summary:\n\n{summary}\n\n要求：专业学术语气，使用 Markdown 格式，分级标题清晰。"
    result = llm.invoke(prompt)   # 保持你原来的 llm 调用
    
    report = result.content
    
    # ==================== 新增参考文献 ====================
    if references:
        refs_md = "\n".join([
            f"{i+1}. [{p['title']}]({p['arxiv_url']}) — {p['authors']}, {p['published']}"
            for i, p in enumerate(references)
        ])
        report += f"""

## 参考文献

{refs_md}

（所有文献均来自 arXiv 实时搜索，可直接点击访问 PDF）
"""
    return report