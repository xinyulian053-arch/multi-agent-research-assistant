import arxiv

def search_arxiv(query, max_results=5):  # 增加到5个，更丰富
    search = arxiv.Search(query=query, max_results=max_results)
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "authors": ", ".join([a.name for a in result.authors]),
            "published": result.published.strftime("%Y"),
            "arxiv_url": result.entry_id,          # ← 标准 arXiv 链接（可点击）
            "pdf_url": result.pdf_url,
            "abstract": result.summary[:300] + "..." if len(result.summary) > 300 else result.summary
        })
    return results