import streamlit as st
from streamlit_ace import st_ace
import random
import time

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

# ----------------------------
# 난이도별 문제
# ----------------------------

PROBLEMS = {
    "초급": [
        'print("Hello World")',

        '''name = "Python"
print(name)''',

        '''x = 10
y = 20
print(x + y)''',

        '''for i in range(5):
    print(i)'''
    ],

    "중급": [
        '''numbers = [1, 2, 3, 4, 5]

for n in numbers:
    print(n * 2)''',

        '''def greet(name):
    return f"Hello {name}"

print(greet("Kim"))''',

        '''try:
    x = int(input())
    print(x)
except ValueError:
    print("Error")'''
    ],

    "고급": [
        '''class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"

p = Person("Alice")
print(p.greet())''',

        '''nums = [1, 2, 3, 4]

squared = list(map(lambda x: x**2, nums))

print(squared)''',

        '''from collections import Counter

text = "banana"

counter = Counter(text)

print(counter)'''
    ]
}

# ----------------------------
# 세션 상태 초기화
# ----------------------------

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "초급"

if "problem" not in st.session_state:
    st.session_state.problem = random.choice(
        PROBLEMS[st.session_state.difficulty]
    )

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ----------------------------
# 제목
# ----------------------------

st.title("⌨️ Python 코드 타자 연습")

st.write("Python 코드를 그대로 입력하세요.")

# ----------------------------
# 난이도 선택
# ----------------------------

difficulty = st.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# 난이도 바뀌면 새 문제
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.problem = random.choice(PROBLEMS[difficulty])
    st.session_state.start_time = None

problem = st.session_state.problem

# ----------------------------
# 문제 표시
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("문제 코드")
    st.code(problem, language="python")

# ----------------------------
# 코드 입력창
# ----------------------------

with col2:
    st.subheader("코드 입력")

    user_input = st_ace(
        placeholder="여기에 Python 코드를 입력하세요...",
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=16,
        tab_size=4,
        show_gutter=True,
        wrap=True,
        auto_update=True,
        height=300
    )

# ----------------------------
# 시간 측정 시작
# ----------------------------

if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# ----------------------------
# 결과 검사
# ----------------------------

if user_input:

    target = problem.strip()
    typed = user_input.strip()

    # 정확도 계산
    correct_chars = sum(
        1 for a, b in zip(target, typed) if a == b
    )

    accuracy = correct_chars / max(len(target), 1) * 100

    st.progress(min(int(accuracy), 100))

    st.write(f"정확도: {accuracy:.2f}%")

    # 완벽히 일치하면 성공
    if typed == target:

        elapsed = time.time() - st.session_state.start_time

        cpm = len(target) / elapsed * 60

        st.success("완벽합니다! 🎉")

        st.write(f"⏱ 시간: {elapsed:.2f}초")
        st.write(f"⚡ 타자 속도: {cpm:.2f} CPM")

        if st.button("다음 문제"):
            st.session_state.problem = random.choice(
                PROBLEMS[difficulty]
            )
            st.session_state.start_time = None
            st.rerun()
