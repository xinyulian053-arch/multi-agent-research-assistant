from tools.arxiv_search import search_arxiv

def search_agent(tasks):
    # 兼容 planner 返回的 list 或 str
    if isinstance(tasks, list):
        query = " ".join(tasks) if tasks else "latest research"
    else:
        query = str(tasks)
    papers = search_arxiv(query)
    return papers   # ← 现在每个 paper 都有 arxiv_url