from tools.pdf_reader import read_pdf_from_url

def reader_agent(papers):

    contents = []

    for paper in papers:
        text = read_pdf_from_url(paper["pdf_url"])
        contents.append(text)

    return contents