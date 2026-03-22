from agents.planner_agent import plan_task
from agents.search_agent import search_agent
from agents.reader_agent import reader_agent
from agents.analyst_agent import analyze
from agents.writer_agent import write_report
from utils.file_utils import save_report, save_pdf

def main():
    topic = input("Enter research topic: ")
    
    print("Planning...")
    tasks = plan_task(topic)
    
    print("Searching papers...")
    papers = search_agent(tasks)
    
    print("Reading papers...")
    contents = reader_agent(papers)
    
    print("Analyzing...")
    summary = analyze(contents)
    
    print("Writing report...")
    report = write_report(summary, topic, papers)
    
    # 保存 Markdown
    save_report(report, topic)
    # 保存 PDF
    save_pdf(report, topic)
    
    print("\n===== Final Report =====")
    print(report)

if __name__ == "__main__":
    main()