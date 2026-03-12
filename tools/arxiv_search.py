import arxiv

def search_arxiv(query, max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results
    )

    results = []

    for result in search.results():
        results.append({
            "title": result.title,
            "pdf_url": result.pdf_url
        })

    return results


# 下面这部分只是测试代码
if __name__ == "__main__":
    papers = search_arxiv("quantum computing")

    for p in papers:
        print(p)