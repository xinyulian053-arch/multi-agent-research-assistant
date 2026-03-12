# analyst_agent.py
from langchain_deepseek import ChatDeepSeek

# 初始化 DeepSeek LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="sk-c9621c51ed704a9daf3309217ea0f046",
    temperature=0.5
)

def analyze(contents):
    prompt = f"""
Summarize the key ideas from the following text:

{contents}
"""
    result = llm.invoke(prompt)
    return result.content