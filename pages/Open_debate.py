import streamlit as st
from prompt import ROUND0_OPEN_SYSTEM, OPEN_DEBATE_SYSTEM, DEFAULT_OPEN_QUESTION, EMOJI_ROLES
from model import Openai_ChatModel, Openai_CompletionModel, Baichuan_Model, Qwen_Model


def display_speech(respond, round, emoji, model_name, speech_order):
    if speech_order % 2 == 1:
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 20px;">
            <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; width: 100%;">
                {respond}
            </div>
            <span style="font-size: 2em; margin-right: 10px;">
                Round{round}<br>{emoji}<br>
                <span style="font-size: 0.5em;">{model_name}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 20px;">
            <span style="font-size: 2em; margin-right: 10px;">
                Round{round}<br>{emoji}<br>
                <span style="font-size: 0.5em;">{model_name}</span>
            </span>
            <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; width: 100%;">
                {respond}
            </div>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    if "open_debaters_count" not in st.session_state:
        st.session_state["open_debaters_count"] = 0
    if "open_debaters" not in st.session_state:
        st.session_state["open_debaters"] = [None] * 2

    # 基本配置
    st.title('辩论设置')
    max_debate_rounds = st.number_input('最大轮数', min_value=1, max_value=20, value=5, step=1)

    # Openai模型
    if "open_openai_api_key" not in st.session_state:
        st.session_state["open_openai_api_key"] = ""
    st.text_input("Openai API Key", key="open_openai_api_key", type="default", value=st.session_state["open_openai_api_key"])
    if "open_openai_position_in_debate" not in st.session_state:
        st.session_state["open_openai_position_in_debate"] = []
    if st.button('添加Openai模型➕'):
        if st.session_state["open_debaters_count"] < 2:
            st.session_state["open_openai_position_in_debate"].append(st.session_state["open_debaters_count"])
            st.session_state["open_debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为2")
    for i in st.session_state["open_openai_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-3.5-turbo-instruct',
                         'gpt-4', 'gpt-4o', 'gpt-4-turbo'], key=f'open_debater_{i}')
            st.number_input('temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'open_temperature_{i}')
            if st.session_state[f'open_debater_{i}'] in ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-4', 'gpt-4o', 'gpt-4-turbo']:
                st.session_state["open_debaters"][i] = Openai_ChatModel(st.session_state['open_openai_api_key'],
                                                                        st.session_state[f'open_debater_{i}'],
                                                                        st.session_state[f'open_temperature_{i}'])
            else:
                st.session_state["open_debaters"][i] = Openai_CompletionModel(st.session_state['open_openai_api_key'],
                                                                              st.session_state[f'open_debater_{i}'],
                                                                              st.session_state[f'open_temperature_{i}'])

    # Baichuan模型
    if "open_baichuan_api_key" not in st.session_state:
        st.session_state["open_baichuan_api_key"] = ""
    st.text_input("Baichuan API Key", key="open_baichuan_api_key", type="default", value=st.session_state["open_baichuan_api_key"])
    if "open_baichuan_position_in_debate" not in st.session_state:
        st.session_state["open_baichuan_position_in_debate"] = []
    if st.button('添加Baichuan模型➕'):
        if st.session_state["open_debaters_count"] < 2:
            st.session_state["open_baichuan_position_in_debate"].append(st.session_state["open_debaters_count"])
            st.session_state["open_debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为2")
    for i in st.session_state["open_baichuan_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['Baichuan2-53B', 'Baichuan2-Turbo-192k', 'Baichuan2-Turbo',
                         'Baichuan3-Turbo-128k', 'Baichuan3-Turbo', 'Baichuan4'], key=f'open_debater_{i}')
            st.number_input('temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'open_temperature_{i}')
            st.session_state["open_debaters"][i] = Baichuan_Model(st.session_state['open_baichuan_api_key'],
                                                                  st.session_state[f'open_debater_{i}'],
                                                                  st.session_state[f'open_temperature_{i}'])

    # Qwen模型
    if "open_qwen_api_key" not in st.session_state:
        st.session_state["open_qwen_api_key"] = ""
    st.text_input("Qwen API Key", key="open_qwen_api_key", type="default", value=st.session_state["open_qwen_api_key"])
    if "open_qwen_position_in_debate" not in st.session_state:
        st.session_state["open_qwen_position_in_debate"] = []
    if st.button('添加Qwen模型➕'):
        if st.session_state["open_debaters_count"] < 2:
            st.session_state["open_qwen_position_in_debate"].append(st.session_state["open_debaters_count"])
            st.session_state["open_debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为2")
    for i in st.session_state["open_qwen_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['qwen-max', 'qwen-max-0428', 'qwen-long',
                                  'qwen2-72b-instruct', 'qwen2-57b-a14b-instruct', 'qwen2-7b-instruct',
                                  'qwen2-1.5b-instruct', 'qwen2-0.5b-instruct', 'qwen-max-longcontext',
                                  'qwen-plus', 'qwen-turbo', 'qwen1.5-110b-chat', 'qwen-7b-chat'], key=f'open_debater_{i}')
            st.number_input('open_temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'open_temperature_{i}')
            st.session_state["open_debaters"][i] = Qwen_Model(st.session_state['open_qwen_api_key'],
                                                              st.session_state[f'open_debater_{i}'],
                                                              st.session_state[f'open_temperature_{i}'])

    # 清除设置
    if st.button('清除设置🧹'):
        for key in st.session_state:
            del st.session_state[key]
        st.rerun()


st.title("🏛️ 开放辩论")
with st.expander("System Prompt设置"):
    if 'open_round0_prompt' not in st.session_state:
        st.session_state['open_round0_prompt'] = ROUND0_OPEN_SYSTEM
    if 'open_system_prompt' not in st.session_state:
        st.session_state['open_system_prompt'] = OPEN_DEBATE_SYSTEM
    st.text_area("Round0 Prompt", height=120, value=st.session_state['open_round0_prompt'], key="open_round0_prompt")
    st.text_area("Debate Prompt", height=120, value=st.session_state['open_system_prompt'], key="open_system_prompt")
if 'open_question' not in st.session_state:
    st.session_state['open_question'] = DEFAULT_OPEN_QUESTION
st.session_state['open_question'] = st.text_area("问题", height=100, value=st.session_state['open_question'])

st.title("🤖🆚👾 辩论过程")
if st.button('开始辩论🎬'):
    if st.session_state["open_debaters_count"] == 2:
        debate_topic = f"Question: {st.session_state['open_question']}\n"
        dialogs = []
        for i in range(max_debate_rounds + 1):
            if i == 0:
                for j in range(st.session_state["open_debaters_count"]):
                    # Round0回答
                    with st.spinner('调用API中...'):
                        respond = st.session_state["open_debaters"][j].round0_open_answer(st.session_state['open_round0_prompt'], debate_topic)
                    dialogs.append(respond)
                    display_speech(respond, 0, EMOJI_ROLES[j], st.session_state["open_debaters"][j].model, j)
            else:
                debater_index = (i - 1) % st.session_state["open_debaters_count"]
                with st.spinner('调用API中...'):
                    respond, agreed = st.session_state["open_debaters"][debater_index].open_debate(st.session_state['open_system_prompt'],
                                                                                                   debate_topic,
                                                                                                   dialogs)
                dialogs.append(respond)
                display_speech(respond, i, EMOJI_ROLES[debater_index], st.session_state["open_debaters"][debater_index].model, debater_index)
                if agreed:
                    break
    else:
        st.error("辩论至少需要2个模型参加")
