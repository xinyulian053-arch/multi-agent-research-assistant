import streamlit as st
import sys
import os
import traceback

# 添加项目根目录到 sys.path（让 import main 和 utils 能找到）
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# 如果 venv 的 site-packages 确实需要（通常不需要，但保留以防万一）
venv_site_packages = os.path.join(project_root, "venv", "Lib", "site-packages")
if os.path.exists(venv_site_packages):
    sys.path.append(venv_site_packages)

# 导入你的 agent 函数和工具
from main import plan_task, search_agent, reader_agent, analyze, write_report
from utils.file_utils import save_report, save_pdf

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("Multi-Agent Research Assistant")
st.markdown("输入研究主题，点击生成按钮，让多代理系统帮你自动完成文献调研与报告撰写。")

# 输入框
topic = st.text_input(
    "请输入研究主题（英文或中文均可）：",
    placeholder="例如：Quantum Computing in 2025 或 2025年的量子计算进展",
    help="主题越具体，报告质量通常越好。"
)

if st.button("生成报告", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("请输入研究主题！")
    else:
        try:
            with st.status("正在生成报告...", expanded=True) as status:
                st.info("1. 规划研究任务...")
                tasks = plan_task(topic)

                st.info("2. 搜索相关论文与资料...")
                papers = search_agent(tasks)

                st.info("3. 阅读并提取关键内容...")
                contents = reader_agent(papers)

                st.info("4. 综合分析内容...")
                summary = analyze(contents)

                st.info("5. 撰写完整报告...")
                report = write_report(summary, topic)

                status.update(label="报告生成完成！正在保存文件...", state="complete")

            # 保存 Markdown 和 PDF
            save_report(report, topic)
            save_pdf(report, topic)

            # 计算文件路径（方便用户知道文件在哪里）
            md_filename = f"{topic.replace(' ', '_')}_report.md"
            pdf_filename = f"{topic.replace(' ', '_')}_report.pdf"

            abs_md = os.path.abspath(md_filename)
            abs_pdf = os.path.abspath(pdf_filename)

            st.success("报告生成成功！")

            # 显示下载按钮
            col1, col2 = st.columns(2)
            with col1:
                with open(md_filename, "rb") as f:
                    st.download_button(
                        label="下载 Markdown 报告",
                        data=f,
                        file_name=md_filename,
                        mime="text/markdown"
                    )
            with col2:
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        label="下载 PDF 报告",
                        data=f,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )

            # 显示报告预览
            st.subheader("报告预览")
            st.markdown("---")
            st.markdown(report)

            # 可选：也显示纯文本区域（方便复制）
            with st.expander("纯文本版本（可复制）", expanded=False):
                st.text_area("完整报告文本", report, height=400)

            st.info(f"文件已保存到当前目录：\n\n"
                    f"- Markdown: {abs_md}\n"
                    f"- PDF: {abs_pdf}")

        except Exception as e:
            st.error("生成过程中出现错误，请检查控制台输出或联系开发者。")
            st.exception(e)
            # 打印详细错误到控制台（开发时有用）
            print("生成报告失败：")
            traceback.print_exc()

st.markdown("---")
st.caption("基于多代理系统 · Powered by Grok & Streamlit")