# analyst_agent.py
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    api_key="sk-c9621c51ed704a9daf3309217ea0f046",  # 替换为你的 Key
    model="deepseek-chat",                          # 必填
    model_kwargs={}                                  # 可选
)

def analyze(contents):
    prompt = f"Summarize the key ideas from the following text:\n\n{contents}"
    result = llm.invoke(prompt)
    return result.content