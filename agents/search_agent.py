from tools.arxiv_search import search_arxiv

def search_agent(query):

    papers = search_arxiv(query)

    return papers