import streamlit as st
from streamlit_ace import st_ace
import random
import time

# ----------------------------
# 페이지 설정
# ----------------------------

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

# ----------------------------
# 문제 데이터
# ----------------------------

PROBLEMS = {
    "초급": [
        '''print("Hello World")''',

        '''name = "Python"
print(name)''',

        '''x = 10
y = 20
print(x + y)''',

        '''for i in range(5):
    print(i)'''
    ],

    "중급": [
        '''numbers = [1, 2, 3]

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
# 세션 상태
# ----------------------------

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "초급"

if "problem" not in st.session_state:
    st.session_state.problem = random.choice(
        PROBLEMS["초급"]
    )

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ----------------------------
# 제목
# ----------------------------

st.title("⌨️ Python 코드 타자 연습")

st.write("Python 코드를 그대로 입력하세요.")

# ----------------------------
# 학생 이름 입력
# ----------------------------

student_name = st.text_input("학생 이름")

# ----------------------------
# 난이도 선택
# ----------------------------

difficulty = st.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# 난이도 변경 시 새 문제
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.problem = random.choice(
        PROBLEMS[difficulty]
    )
    st.session_state.start_time = None

problem = st.session_state.problem

# ----------------------------
# 문제 / 입력창
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("문제 코드")
    st.code(problem, language="python")

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
# 시작 시간 기록
# ----------------------------

if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# ----------------------------
# 결과 확인 버튼
# ----------------------------

if st.button("결과 확인"):

    if not student_name:
        st.warning("학생 이름을 입력하세요.")
        st.stop()

    if not user_input:
        st.warning("코드를 입력하세요.")
        st.stop()

    target = problem.strip()
    typed = user_input.strip()

    # 정확도 계산
    correct_chars = sum(
        1 for a, b in zip(target, typed) if a == b
    )

    accuracy = (
        correct_chars / max(len(target), 1)
    ) * 100

    # 시간 계산
    elapsed = time.time() - st.session_state.start_time

    # 타수 계산
    cpm = len(typed) / elapsed * 60

    st.divider()

    st.subheader("📊 결과")

    st.write(f"👨‍🎓 학생 이름: {student_name}")
    st.write(f"📚 난이도: {difficulty}")
    st.write(f"⏱ 걸린 시간: {elapsed:.2f}초")
    st.write(f"⚡ 타자 속도: {cpm:.2f} CPM")
    st.write(f"🎯 정확도: {accuracy:.2f}%")

    # 성공 여부
    if typed == target:
        st.success("완벽하게 입력했습니다! 🎉")
    else:
        st.error("오타가 있습니다.")

# ----------------------------
# 다음 문제 버튼
# ----------------------------

if st.button("다음 문제"):

    st.session_state.problem = random.choice(
        PROBLEMS[difficulty]
    )

    st.session_state.start_time = None

    st.rerun()
