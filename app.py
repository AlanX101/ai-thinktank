import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# ============ 模型配置（想换模型改这里就行） ============
MODEL_GPT = "gpt-4o"                            # OpenAI
MODEL_GEMINI = "gemini/gemini-2.5-pro"          # Google Gemini
MODEL_GROK = "xai/grok-4"                       # xAI Grok
MODEL_CLAUDE = "anthropic/claude-sonnet-4-5"    # Anthropic Muse
# =======================================================

st.set_page_config(page_title="AI 智囊团", layout="wide", page_icon="🏛️")

# 初始化历史消息列表
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏与清空按钮
with st.sidebar:
    st.header("⚙️ 控制面板")
    st.write(f"当前对话轮数: {len(st.session_state.messages) // 2}")
    if st.button("🗑️ 清空所有对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🏛️ 四人 AI 战略智囊团")
st.caption("GPT（架构）· Muse（创意）· Grok（质检）· Gemini（统筹）")

# 显示历史对话记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用户输入
user_input = st.chat_input("输入你想探讨的事情或问题...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("智囊团正在头脑风暴并推演中..."):
            try:
                # 优先从 Streamlit Secrets 读取密钥，其次读本地 .env
                def get_key(name):
                    try:
                        return st.secrets.get(name, os.getenv(name, ""))
                    except Exception:
                        return os.getenv(name, "")

                openai_key = get_key("OPENAI_API_KEY")
                gemini_key = get_key("GEMINI_API_KEY")
                xai_key = get_key("XAI_API_KEY")
                anthropic_key = get_key("ANTHROPIC_API_KEY")

                llm_gpt = LLM(model=MODEL_GPT, api_key=openai_key)
                llm_gemini = LLM(model=MODEL_GEMINI, api_key=gemini_key)
                llm_grok = LLM(model=MODEL_GROK, api_key=xai_key)
                llm_claude = LLM(model=MODEL_CLAUDE, api_key=anthropic_key)

                architect = Agent(role="GPT 架构师", goal="制定严密方案与落地节奏", backstory="顶尖商业顾问", llm=llm_gpt)
                creative = Agent(role="Claude 创意官", goal="在方案基础上发散出差异化创意与破局思路", backstory="天马行空的创意总监", llm=llm_claude)
                critic = Agent(role="Grok 质检官", goal="反向找漏洞与非共识破局", backstory="敏锐极客", llm=llm_grok)
                coordinator = Agent(role="Gemini 统筹官", goal="综合全员建议并输出落地清单", backstory="执行统筹", llm=llm_gemini)

                t1 = Task(description=f"针对【{user_input}】制定核心方案框架", expected_output="架构规划", agent=architect)
                t2 = Task(description="基于架构师的方案，发散补充差异化创意、亮点打法与意外破局点", expected_output="创意增补案", agent=creative)
                t3 = Task(description="对架构方案与创意增补进行反向挑刺，指出潜在陷阱与被忽略的风险", expected_output="审查备忘录", agent=critic)
                t4 = Task(description="综合架构、创意与审查意见，输出最终落地执行清单：步骤、优先级、时间节奏", expected_output="最终定案报告", agent=coordinator)

                crew = Crew(agents=[architect, creative, critic, coordinator], tasks=[t1, t2, t3, t4], process=Process.sequential)
                result = str(crew.kickoff())

                st.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                st.error(f"运行出错，请检查 API Key 是否配置正确: {str(e)}")
