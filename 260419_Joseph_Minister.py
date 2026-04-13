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

if "church" not in st.session_state: st.session_state["church"] = ""
if "dept" not in st.session_state: st.session_state["dept"] = ""
if "students" not in st.session_state: st.session_state["students"] = ""
if "messages" not in st.session_state: st.session_state["messages"] = []
if "page" not in st.session_state: st.session_state["page"] = 1

def get_chatgpt_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state["messages"],
    )
    
    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    return answer

if st.session_state["page"] == 1:
    st.title("12과: 요셉을 인도하시는 분은 누구일까요?")
    
    church = st.text_input("교회명 (예: 1516교회)", value=st.session_state["church"])
    dept = st.text_input("부서명 (예: 소년부)", value=st.session_state["dept"])
    students = st.text_input("학생 명단", value=st.session_state["students"])
    
    if st.button("활동 시작하기"):
        if church and dept and students:
            st.session_state["church"] = church
            st.session_state["dept"] = dept
            st.session_state["students"] = students
            
            full_prompt = (
                f"당신은 성경 등장인물 중 총리가 되어 다시 형제들과 만난 시기의 요셉입니다."
                f"{church} {dept} 학생들이 소그룹 활동 과정에서 당신을 인터뷰할 것입니다. "
                f"교회 이름은 {church}, 학생 이름은 {students}입니다."
                "공과 제목은 '요셉을 인도하시는 분은 누구일까요?'이고, 본문은 창세기 45장 1-8절입니다. 이 내용을 중심으로 인터뷰에 응해주세요."
                "다음의 수업 진행 가이드를 참고하세요: 하나님은 인간의 죄와 악을 선으로 바꾸셨고, 요셉을 사용하셔서 야곱 가족의 생명과 그 후손들의 생명을 보존하셨다. 요셉이 뛰어나고 유능해서 애굽의 총리가 된 것이 아니다. 매 순간 역사하신 하나님으로 인해 요셉과 그의 가정과 온 이스라엘이 복을 받게 되었다. 요셉은 이러한 과정을 겪으면서 하나님의 인도하심을 알 수 있었고, 하나님께 자신의 인생을 맡기게 되었다. 우리 역시 인생을 나의 시각이 아닌 하나님의 관점으로 바라보는 믿음을 배워야 한다. 가정에서, 학교에서, 교회에서 여러 상황 가운데 때로는 이해하기 어렵고 힘든 일이 있을지라도 하나님이 나와 함께하시고 내 삶을 인도하신다는 확신이 있어야 할 것이다."
                "교리의 기준은 한국 장로교단입니다."
                "초등학생들이 이해할 수 있도록 한 줄 정도로 간결하고 쉽게 말하세요. 인터뷰하는 태도로 존대말을 사용하세요."
            )
            st.session_state["messages"] = [{"role": "system", "content": full_prompt}]
            st.session_state["page"] = 2
            st.rerun()
else:
    st.title("12과: 요셉을 인도하시는 분은 누구일까요?")

    col1, col2 = st.columns(2)

    with col1:
        st.write("하나님께서 요셉을 애굽으로 인도하셨어요.")
        st.image("https://i.imgur.com/fVVIoL0.png", use_container_width=True)

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