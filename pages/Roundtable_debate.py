import streamlit as st
from prompt import ROUND0_SYSTEM, ROUNDTABLE_DEBATE_SYSTEM, DEFAULT_QUESTION, DEFAULT_OPTIONS, EMOJI_ROLES
from model import Openai_ChatModel, Openai_CompletionModel, Baichuan_Model, Qwen_Model


def display_speech(emoji, model_name, answer, argument, round):
    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; justify-content: flex-start; margin-bottom: 20px;">
        <span style="font-size: 1.5em; margin-right: 10px;">
            Round{round}<br>{emoji}<br>
            <span style="font-size: 0.75em; display: block;">{model_name}</span>
        </span>
        <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; width: 100%;">
            <b>立场: <span style="color: red;">{answer}</span><br>论据: </b>{argument}
        </div>
    </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    if "debaters_count" not in st.session_state:
        st.session_state["debaters_count"] = 0
    if "debaters" not in st.session_state:
        st.session_state["debaters"] = [None] * 4

    # 基本配置
    st.title('辩论设置')
    max_debate_rounds = st.number_input('最大轮数', min_value=1, max_value=20, value=5, step=1)

    # Openai模型
    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = ""
    st.text_input("Openai API Key", key="openai_api_key", type="default", value=st.session_state["openai_api_key"])
    if "openai_position_in_debate" not in st.session_state:
        st.session_state["openai_position_in_debate"] = []
    if st.button('添加Openai模型➕'):
        if st.session_state["debaters_count"] < 4:
            st.session_state["openai_position_in_debate"].append(st.session_state["debaters_count"])
            st.session_state["debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为4")
    for i in st.session_state["openai_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-3.5-turbo-instruct',
                         'gpt-4', 'gpt-4o', 'gpt-4-turbo'], key=f'debater_{i}')
            st.number_input('temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'temperature_{i}')
            if st.session_state[f'debater_{i}'] in ['gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'gpt-4', 'gpt-4o', 'gpt-4-turbo']:
                st.session_state["debaters"][i] = Openai_ChatModel(st.session_state['openai_api_key'],
                                                                   st.session_state[f'debater_{i}'],
                                                                   st.session_state[f'temperature_{i}'])
            else:
                st.session_state["debaters"][i] = Openai_CompletionModel(st.session_state['openai_api_key'],
                                                                         st.session_state[f'debater_{i}'],
                                                                         st.session_state[f'temperature_{i}'])

    # Baichuan模型
    if "baichuan_api_key" not in st.session_state:
        st.session_state["baichuan_api_key"] = ""
    st.text_input("Baichuan API Key", key="baichuan_api_key", type="default", value=st.session_state["baichuan_api_key"])
    if "baichuan_position_in_debate" not in st.session_state:
        st.session_state["baichuan_position_in_debate"] = []
    if st.button('添加Baichuan模型➕'):
        if st.session_state["debaters_count"] < 4:
            st.session_state["baichuan_position_in_debate"].append(st.session_state["debaters_count"])
            st.session_state["debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为4")
    for i in st.session_state["baichuan_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['Baichuan2-53B', 'Baichuan2-Turbo-192k', 'Baichuan2-Turbo',
                         'Baichuan3-Turbo-128k', 'Baichuan3-Turbo', 'Baichuan4'], key=f'debater_{i}')
            st.number_input('temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'temperature_{i}')
            st.session_state["debaters"][i] = Baichuan_Model(st.session_state['baichuan_api_key'],
                                                             st.session_state[f'debater_{i}'],
                                                             st.session_state[f'temperature_{i}'])

    # Qwen模型
    if "qwen_api_key" not in st.session_state:
        st.session_state["qwen_api_key"] = ""
    st.text_input("Qwen API Key", key="qwen_api_key", type="default", value=st.session_state["qwen_api_key"])
    if "qwen_position_in_debate" not in st.session_state:
        st.session_state["qwen_position_in_debate"] = []
    if st.button('添加Qwen模型➕'):
        if st.session_state["debaters_count"] < 4:
            st.session_state["qwen_position_in_debate"].append(st.session_state["debaters_count"])
            st.session_state["debaters_count"] += 1
        else:
            st.error("参辩模型数量上限为4")
    for i in st.session_state["qwen_position_in_debate"]:
        with st.expander(f"LLM {i + 1}"):
            st.selectbox('type', ['qwen-max', 'qwen-max-0428', 'qwen-long',
                                  'qwen2-72b-instruct', 'qwen2-57b-a14b-instruct', 'qwen2-7b-instruct',
                                  'qwen2-1.5b-instruct', 'qwen2-0.5b-instruct', 'qwen-max-longcontext',
                                  'qwen-plus', 'qwen-turbo', 'qwen1.5-110b-chat', 'qwen-7b-chat'], key=f'debater_{i}')
            st.number_input('temperature', min_value=0.0, max_value=1.0,
                            value=0.0, step=0.1, key=f'temperature_{i}')
            st.session_state["debaters"][i] = Qwen_Model(st.session_state['qwen_api_key'],
                                                         st.session_state[f'debater_{i}'],
                                                         st.session_state[f'temperature_{i}'])

    # 清除设置
    if st.button('清除设置🧹'):
        for key in st.session_state:
            del st.session_state[key]
        st.rerun()


st.title("🏛️ 圆桌辩论")
with st.expander("System Prompt设置"):
    if 'round0_prompt' not in st.session_state:
        st.session_state['round0_prompt'] = ROUND0_SYSTEM
    if 'system_prompt' not in st.session_state:
        st.session_state['system_prompt'] = ROUNDTABLE_DEBATE_SYSTEM
    st.text_area("Round0 Prompt", height=120, value=st.session_state['round0_prompt'], key="round0_prompt")
    st.text_area("Debate Prompt", height=120, value=st.session_state['system_prompt'], key="system_prompt")
if 'question' not in st.session_state:
    st.session_state['question'] = DEFAULT_QUESTION
if 'options' not in st.session_state:
    st.session_state['options'] = DEFAULT_OPTIONS
st.session_state['question'] = st.text_area("问题", height=100, value=st.session_state['question'])
st.session_state['options'] = st.text_area("选项", height=50, value=st.session_state['options'])

st.title("🗣辩论过程")
if st.button('开始辩论🎬'):
    if st.session_state["debaters_count"] >= 2:
        debate_topic = f"Question: {st.session_state['question']}\nOptions: {st.session_state['options']}"
        dialogs = []
        viewpoints = []
        for i in range(max_debate_rounds + 1):
            if i == 0:
                for j in range(st.session_state["debaters_count"]):
                    # Round0回答
                    with st.spinner('调用API中...'):
                        answer, argument, respond = st.session_state["debaters"][j].round0_answer(st.session_state['round0_prompt'], debate_topic)
                    dialogs.append({"role": f"debater{j + 1}", "content": respond})
                    viewpoints.append(answer)
                    display_speech(EMOJI_ROLES[j], st.session_state["debaters"][j].model, answer, argument, 0)
                if len(set(viewpoints[-st.session_state["debaters_count"]:])) == 1:
                    break
            else:
                debater_index = (i - 1) % st.session_state["debaters_count"]
                with st.spinner('调用API中...'):
                    answer, argument, respond = st.session_state["debaters"][debater_index].roundtable_debate(st.session_state['system_prompt'],
                                                                                                              debate_topic, dialogs,
                                                                                                              st.session_state["debaters_count"],
                                                                                                              role=f"debater{debater_index + 1}")
                dialogs.append({"role": f"debater{debater_index + 1}", "content": respond})
                viewpoints.append(answer)
                display_speech(EMOJI_ROLES[debater_index], st.session_state["debaters"][debater_index].model, answer, argument, i)
                if len(set(viewpoints[-st.session_state["debaters_count"]:])) == 1:
                    break
    else:
        st.error("辩论至少需要2个模型参加")
