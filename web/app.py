import streamlit as st


st.set_page_config(
    page_title="Research Assistant 已迁移",
    page_icon="🔎",
    layout="centered",
)

st.title("前端已迁移到 Vue")
st.write(
    "这个项目现在使用 FastAPI + Vue 作为主界面。"
    "Streamlit 入口仅保留为兼容提示。"
)

st.code("venv\\Scripts\\python.exe -m uvicorn api.app:app --reload --host 127.0.0.1 --port 8000")
st.code("cd frontend\nnpm install\nnpm run dev")

st.info("启动后访问 http://127.0.0.1:5173 使用新的研究工作台。")
