import streamlit as st
from prompt import ROUND0_SYSTEM, DUAL_DEBATE_SYSTEM, DEFAULT_QUESTION
from model import Openai_ChatModel, Openai_CompletionModel, Baichuan_Model, Qwen_Model


def display_speech(answer, argument, round, role):
    if role % 2 == 1:
        st.markdown(f"""
                <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 20px;">
                    <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; width: 100%;">
                        <b>Stance: <span style="color: red;">{answer}</span><br>Argument: </b>{argument}
                    </div><span style="font-size: 2em; margin-right: 10px;">Round{round}<br>👾</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 20px;">
                <span style="font-size: 2em; margin-right: 10px;">Round{round}<br>🤖</span>
                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; width: 100%;">
                    <b>Stance: <span style="color: red;">{answer}</span><br>Argument: </b>{argument}
                </div>
            </div>
            """, unsafe_allow_html=True)


with st.sidebar:
    if "debaters_count" not in st.session_state:
        st.session_state["debaters_count"] = 0
    debaters = [None] * (st.session_state["debaters_count"] + 1)

    # 基本配置
    st.title('General Configuration')
    max_debate_rounds = st.number_input('Maximum Number of Debate Rounds', min_value=1, max_value=20, value=5, step=1)

    # Openai模型
    openai_api_key = st.text_input("Openai API Key", key="openai_api_key", type="password")
    if "openai_position_in_debate" not in st.session_state:
        st.session_state["openai_position_in_debate"] = []
    if st.button('Add Openai Model➕') and st.session_state["debaters_count"] < 2:
        st.session_state["openai_position_in_debate"].append(st.session_state["debaters_count"])
        st.session_state["debaters_count"] += 1
    for i in st.session_state["openai_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            type = st.selectbox('type', ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-3.5-turbo-instruct',
                                'gpt-4', 'gpt-4o', 'gpt-4-turbo'], key=f'debater_{i}')
            temperature = st.number_input('temperature', min_value=0.0, max_value=1.0,
                                          value=0.0, step=0.1, key=f'temperature_{i}')
            if type in ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-4', 'gpt-4o', 'gpt-4-turbo']:
                debaters[i] = Openai_ChatModel(openai_api_key, type, temperature)
            else:
                debaters[i] = Openai_CompletionModel(openai_api_key, type, temperature)

    # Baichuan模型
    baichuan_api_key = st.text_input("Baichuan API Key", key="baichuan_api_key", type="password")
    if "baichuan_position_in_debate" not in st.session_state:
        st.session_state["baichuan_position_in_debate"] = []
    if st.button('Add Baichuan Model➕') and st.session_state["debaters_count"] < 2:
        st.session_state["baichuan_position_in_debate"].append(st.session_state["debaters_count"])
        st.session_state["debaters_count"] += 1
    for i in st.session_state["baichuan_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            type = st.selectbox('type', ['Baichuan2-53B', 'Baichuan2-Turbo-192k', 'Baichuan2-Turbo',
                                'Baichuan3-Turbo-128k', 'Baichuan3-Turbo', 'Baichuan4'], key=f'debater_{i}')
            temperature = st.number_input('temperature', min_value=0.0, max_value=1.0,
                                          value=0.0, step=0.1, key=f'temperature_{i}')
            debaters[i] = Baichuan_Model(baichuan_api_key, type, temperature)

    # Qwen模型
    qwen_api_key = st.text_input("Qwen API Key", key="qwen_api_key", type="password")
    if "qwen_position_in_debate" not in st.session_state:
        st.session_state["qwen_position_in_debate"] = []
    if st.button('Add Qwen Model➕') and st.session_state["debaters_count"] < 2:
        st.session_state["qwen_position_in_debate"].append(st.session_state["debaters_count"])
        st.session_state["debaters_count"] += 1
    for i in st.session_state["qwen_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            type = st.selectbox('type', ['qwen-max', 'qwen-max-0428', 'qwen-long',
                                         'qwen2-72b-instruct', 'qwen2-57b-a14b-instruct', 'qwen2-7b-instruct',
                                         'qwen2-1.5b-instruct', 'qwen2-0.5b-instruct', 'qwen-max-longcontext',
                                         'qwen-plus', 'qwen-turbo', 'qwen1.5-110b-chat', 'qwen-7b-chat'], key=f'debater_{i}')
            temperature = st.number_input('temperature', min_value=0.0, max_value=1.0,
                                          value=0.0, step=0.1, key=f'temperature_{i}')
            debaters[i] = Qwen_Model(qwen_api_key, type, temperature)

st.title("🏛️ LLM Dual Debate")
round0_prompt = st.text_area("Round0 Prompt", height=120, value=ROUND0_SYSTEM)
system_prompt = st.text_area("Debate Prompt", height=120, value=DUAL_DEBATE_SYSTEM)
question = st.text_area("Question", height=120, value=DEFAULT_QUESTION)

st.title("🤖🆚👾 Debate Process")
if st.button('Start Debate') and st.session_state["debaters_count"] == 2:
    dialogs = []
    viewpoints = []
    for i in range(max_debate_rounds + 1):
        if i == 0:
            for j in range(st.session_state["debaters_count"]):
                # Round0回答
                with st.spinner('调用API中...'):
                    answer, argument, respond = debaters[j].round0_answer(round0_prompt, question)
                dialogs.append({"role": f"debater{j + 1}", "content": respond})
                viewpoints.append(answer)
                display_speech(answer, argument, 0, j)
            if len(set(viewpoints[-st.session_state["debaters_count"]:])) == 1:
                break

        else:
            debater_index = (i - 1) % st.session_state["debaters_count"]
            with st.spinner('调用API中...'):
                answer, argument, respond = debaters[debater_index].roundtable_debate(system_prompt, question, dialogs,
                                                                                      st.session_state["debaters_count"],
                                                                                      role=f"debater{debater_index + 1}")
            dialogs.append({"role": f"debater{debater_index + 1}", "content": respond})
            viewpoints.append(answer)
            display_speech(answer, argument, i, debater_index)
            if len(set(viewpoints[-st.session_state["debaters_count"]:])) == 1:
                break
    if viewpoints[-1] == viewpoints[-2]:
        st.markdown(f"""<div style="font-size: 36px;">
                            🤝Agreed on option <span style="color: red;"><b>{viewpoints[-1]}</b></span>
                        </div>""", unsafe_allow_html=True)
