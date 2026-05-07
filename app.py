import streamlit as st
import random
import time

# 연습 문장 리스트
sentences = [
    "Python is a powerful programming language.",
    "Streamlit makes web apps easy.",
    "Practice typing every day.",
    "GitHub is useful for version control.",
    "Coding improves problem solving skills."
]

st.set_page_config(page_title="타자 연습 앱", page_icon="⌨️")

st.title("⌨️ Python 타자 연습")
st.write("문장을 보고 그대로 입력하세요!")

# 세션 상태 초기화
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

sentence = st.session_state.sentence

# 문제 표시
st.subheader("연습 문장")
st.code(sentence)

# 입력창
user_input = st.text_input("여기에 입력하세요")

# 시작 시간 기록
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 결과 확인
if user_input:
    if user_input == sentence:
        end_time = time.time()
        elapsed = end_time - st.session_state.start_time

        # 타수 계산 (분당 문자수 기준)
        speed = len(sentence) / elapsed * 60

        st.success("정답입니다! 🎉")
        st.write(f"⏱ 걸린 시간: {elapsed:.2f}초")
        st.write(f"⚡ 타자 속도: {speed:.2f} CPM")

        if st.button("다음 문제"):
            st.session_state.sentence = random.choice(sentences)
            st.session_state.start_time = None
            st.rerun()

    else:
        # 오타 표시
        st.warning("계속 입력해보세요!")
