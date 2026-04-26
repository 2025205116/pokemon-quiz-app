import streamlit as st


st.set_page_config(page_title="포켓몬 도감 퀴즈")


st.title("포켓몬 도감 퀴즈 앱")
st.markdown("### 제출자: 2025205116 이재혁") 
st.markdown("---")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0


@st.cache_data
def load_quiz_data():
    return [
        {
            "question": "자랑스런 뿔을 상대의 배 밑에 비틀어 박고 한번에 들어올려 집어던져 버리는 천하장사.\n\n 달콤한 꿀을 아주 좋아해서 혼자 독차지하기 위하여 자랑스런 뿔을 써서 상대를 내동댕이친다. ",
            "hint": "힌트: 뿔이 특징인 벌레,격투타입 포켓몬입니다. (초성: ㅎㄹㅋㄹㅅ)",
            "answer": "헤라크로스"
        },
        {
            "question": "문제 B: 어떤 것이든 변신할 수 있다. 잘 때는 돌로 변신해서 공격받지 않도록 하고 있다.\n\n 전신의 세포를 재구성해서 본 것과 똑같이 변신하지만 힘이 빠지면 원래로 돌아간다.",
            "hint": "힌트: 최근에 관련된 게임이 등장해 인기를 끌었다. (초성: ㅁㅌㅁ)",
            "answer": "메타몽"
        },
        {
            "question": "문제 C: 겨우 둔갑했는데 목이 부러져버렸다. 안은 아마도 아직 멀쩡하겠지만 슬프다. \n\n 무시무시한 모습을 누더기로 가리고 사람이나 다른 포켓몬에게 다가가는 외로움이 많은 포켓몬이다.",
            "hint": "힌트: 탈포켓몬이다. (초성: ㄸㄹㅋ)",
            "answer": "따라큐"
        }
    ]

quiz_data = load_quiz_data()


# 미리 정의된 사용자 정보 (딕셔너리 형태)
user_db = {
    "지우": "1234",
    "이슬": "0000",
    "오키드": "1111"
}

def login_section():
    st.subheader("로그인")
    st.write("포켓몬 트레이너 인증을 해주세요.")
    
    username = st.text_input("트레이너 이름:")
    password = st.text_input("비밀번호:", type="password")

    if st.button("로그인"):
        # 입력한 아이디가 user_db에 있고, 비밀번호도 일치하는지 확인!
        if username in user_db and user_db[username] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("등록되지 않은 트레이너이거나 비밀번호가 틀렸습니다.")


def quiz_section():
    st.write(f"총 **{len(quiz_data)}** 개의 문제가 준비되어 있습니다.")
    

    if st.session_state.current_q < len(quiz_data):
        current_data = quiz_data[st.session_state.current_q]
        
        st.progress((st.session_state.current_q) / len(quiz_data))
        st.markdown(f"### 질문 {st.session_state.current_q + 1}")

      
        st.info(current_data["question"])

    
        if st.session_state.attempts >= 1:
            st.warning(current_data["hint"])

       
        user_answer = st.text_input("정답을 입력하세요:", key=f"q_{st.session_state.current_q}")

        if st.button("정답"):
            if user_answer.strip() == current_data["answer"]:
                st.success("정답입니다! 🎉")
                st.session_state.score += 1
                st.session_state.current_q += 1
                st.session_state.attempts = 0 
                st.rerun()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts == 1:
                    st.error("오답입니다. 힌트를 확인하고 다시 시도해보세요!")
                else:
                    st.error(f"또 오답입니다! 정답은 '{current_data['answer']}' 였습니다. 다음 문제로 넘어갑니다. 😢")
                    st.session_state.current_q += 1
                    st.session_state.attempts = 0
                st.rerun()
    
   
    else:
        st.balloons()
        st.subheader("퀴즈 종료!")
        st.write(f"당신의 최종 점수는 **{st.session_state.score} / {len(quiz_data)}** 점 입니다.")
        
        if st.button("처음부터 다시 풀기"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.attempts = 0
            st.rerun()


if not st.session_state.logged_in:
    login_section()
else:
    col1, col2 = st.columns([8, 2])
    with col1:
        st.write("✅ 로그인 성공")
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.attempts = 0
            st.rerun()
            
    st.markdown("---")
    quiz_section()
