from agents.planner_agent import plan_task
from agents.search_agent import search_agent
from agents.reader_agent import reader_agent
from agents.analyst_agent import analyze
from agents.writer_agent import write_report


query = input("Enter research topic: ")

print("Planning...")

steps = plan_task(query)

print("Searching papers...")

papers = search_agent(query)

print("Reading papers...")

contents = reader_agent(papers)

print("Analyzing...")

summary = analyze(contents)

print("Writing report...")

report = write_report(summary, query)

print("\n===== Final Report =====\n")

print(report)