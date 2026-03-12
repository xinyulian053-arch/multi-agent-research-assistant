# writer_agent.py
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="sk-c9621c51ed704a9daf3309217ea0f046",
    temperature=0.5
)

def write_report(summary, topic):
    prompt = f"""
Write a research report about {topic}

Based on this summary:

{summary}
"""
    result = llm.invoke(prompt)
    return result.content