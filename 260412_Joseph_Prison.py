import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import html

st.set_page_config(layout="wide")

load_dotenv()

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MODEL = 'gpt-4o'

client = OpenAI(api_key=OPENAI_API_KEY)

initial_prompt = (
    "당신은 성경 등장인물 중 감옥에 갇힌 시기의 요셉입니다."
    "1516교회 주일학교의 초등학교 5학년 4반 학생들이 소그룹 활동 과정에서 당신을 인터뷰할 것입니다. 교회 이름은 1516교회, 학생 이름은 권준, 김세훈, 나이준, 박윤우 등 4명입니다."
    "당신은 형들의 시기로 인해 노예로 팔려가고, 그곳에서 또 감옥에 갇힌 요셉으로서 인터뷰를 해주게 됩니다."
    "공과 제목은 '형통이란 무엇일까요?'이고, 본문은 창세기 39장 1-5절, 21-23절입니다. 이 내용을 중심으로 인터뷰에 응해주세요."
    "다음의 수업 진행 가이드를 참고하세요: 요셉은 원래 부족한 것 없이 풍족하게 사랑받는 아들이었어요. 하지만 형들의 미움을 사 애굽 사람 보디발의 종으로 팔려갔어요. 그리고 보디발의 집에서도 모함을 받아 죄수가 되었어요. 그런데 성경을 보면 이상한 점 한 가지 있어요. 누가 봐도 그의 인생은 점점 더 힘들고 어려워져 가는데, 성경은 형통하다고 말씀하고 있어요. 바로 하나님께서 요셉과 함께 하셨기 때문이에요. 이처럼 일이 잘되고, 안 되는 것이 형통의 기준이 아니에요. 진정한 형통은 어떤 상황 속에서도 하나님께서 함께 하시는 것이에요."
    "교리의 기준은 한국 장로교단입니다."
    "초등학생들이 이해할 수 있도록, 전체적으로 말을 간결하고 쉽게 하세요. 인터뷰하는 태도로 존대말을 사용하세요."
)

def get_chatgpt_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state["messages"],
    )
    
    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    return answer

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": initial_prompt}]

st.title("11과: 형통이란 무엇일까요?")

col1, col2 = st.columns(2)

with col1:
    st.write("형통은 어떤 상황 속에서도 하나님께서 함께하시는 것이에요.")
    st.image("https://i.imgur.com/ZuGckmT.png", use_container_width=True)

with col2:
#    st.subheader("🎤 인터뷰 내용")
    
    st.markdown("""
        <style>
        div[data-testid="stBottom"] {
            position: static !important;
            width: 100% !important;
            padding: 0px !important;
        }
        div[data-testid="stChatInput"] {
            padding: 10px 0px !important;
        }
        .main .block-container {
            padding-bottom: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    chat_container = st.container(height=300)

    with chat_container:
        for m in st.session_state["messages"]:
            if m["role"] == "system":
                continue
            if m["role"] == "user":
                with st.chat_message("user", avatar="🙋‍♂️"):
                    st.markdown(m["content"])
            elif m["role"] == "assistant":
                with st.chat_message("assistant", avatar="👨‍🌾"):
                    st.markdown(m["content"])

if user_input := st.chat_input("인터뷰 질문을 입력하세요"):
    get_chatgpt_response(user_input)
    st.rerun()